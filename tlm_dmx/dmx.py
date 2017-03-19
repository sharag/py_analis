import time
from bitstring import Bits, BitArray
from bitreader import Bitreader

# ОПИСАНИЕ СПИСКА channels
# [
# [COMMUTID,    - 0
#  CNAME,       - 1
#  PARENT,      - 2
#  FRBITLEN,    - 3
#  WBITLEN,     - 4
#  FREQFR,      - 5
#  SIGNTYPE,    - 6
#  [WORDTABLE], - 7   // [[WORDID, BITPOSINPARENT, WBITLEN],следующее слово, ...] если таблицы нет, то ''
#  [MARKERS]    - 8   // [[MARKERID, BITLEN, MVALUE, BITOFFSET],следующий маркер, ...] если маркеров нет, то ''
#  ],
#  следующий коммутатор, ...]      
#  
class Demuxer:
    def __init__(self, channels, lvl_commut, fname_gts, revers):
        self.channels = channels
        self.fname_gts = fname_gts
        self.lvl_commut = lvl_commut  # уровень текущего коммутатора
        self.revers = revers  # Признак реверса читаемых из файла байт
        self.marker_len = None
        self.used_markers = self.select_markers()  # Перечень искомых маркеров (только с нулевым смещением)
        self.marker = Bits() # Тот маркер, который будет найден в ГТС
        self.cur_fr_bitpos = 0  # Текущая битовая позиция в кадре для выдачи
        self.blen_over_fr = 0  # количество бит, запрашиваемых сверх размера кадра
        if (self.lvl_commut + 1) == len(self.channels):  # Если это последний уровень, то источник - это файл
            try:
                self.sourse = Bitreader(self.fname_gts, self.revers)
            except BaseException as err:
                raise BaseException(err)
        else:  # Если это не последний уровень, то источник - демультиплексор следующего уровня
            self.parent_frame = BitArray(uint=0, length=self.channels[self.lvl_commut + 1][3])  # Буффер для старшего кадра
            try:
                self.sourse = Demuxer(self.channels, self.lvl_commut + 1, self.fname_gts, self.revers)
            except BaseException as err:
                raise BaseException(err)
        self.frame = BitArray(uint=0, length=self.channels[self.lvl_commut][3])  # Буффер для кадра
        self.frame_new = BitArray(uint=0, length=self.channels[self.lvl_commut][3])
        self.frame_temp = BitArray()
        self.frame_num = 0
        
    def get_2frames(self):
        try:
            self.get_frame()
        except BaseException as e:
            print(e)
        self.frame_temp = self.frame
        self.frame = self.frame_new
        self.frame_new = self.frame_temp
        self.get_frame()
        
    def select_markers(self):
        tab = []
        if len(self.channels[self.lvl_commut][8]) > 0:
            self.marker_len = self.channels[self.lvl_commut][8][0][1]
            for i in range(len(self.channels[self.lvl_commut][8])):
                if self.channels[self.lvl_commut][8][i][3] == 0:
                    tab.append(self.channels[self.lvl_commut][8][i])
                    tab[len(tab) - 1].append(bin(int(self.channels[self.lvl_commut][8][i][2],16)))
        return tab

    def get_bits(self, n):
        # Если запрашиваемая последовательность перескакивает на следующий кадр
        if (self.cur_fr_bitpos + n) > self.channels[self.lvl_commut][3]:
            value = BitArray(uint=0, length=n)
            value = self.frame[self.cur_fr_bitpos:self.channels[self.lvl_commut][3]] + self.frame_new[0:(n - (self.channels[self.lvl_commut][3] - self.cur_fr_bitpos))]
            self.frame_temp = self.frame
            self.frame = self.frame_new
            self.frame_new = self.frame_temp
            self.cur_fr_bitpos = n - (self.channels[self.lvl_commut][3] - self.cur_fr_bitpos)
            try:
                self.get_frame()
            except ValueError as err:
                raise ValueError(err)
            return value
        # Если считанного объема хватает для выдачи битовой последовательности, то выдаем
        else:
            begin_pos = self.cur_fr_bitpos
            self.cur_fr_bitpos += n
            return self.frame[begin_pos:self.cur_fr_bitpos]

    def get_frame(self):
        self.cur_frame_len = 0
        self.frame_num += 1
        # Если нужна синхронизация, то поиск маркеров
        if self.marker.len > 0:
            try:
                self.find_sinhr()
            except ValueError as err:
                raise ValueError(err)
        elif len(self.channels[self.lvl_commut][8]) > 0:
            try:
                self.find_sinhr()
            except ValueError as err:
                raise ValueError(err)
        # Если синхра уже найдена чтение всего кадра
        # Если нет word_tables,
        if len(self.channels[self.lvl_commut][7]) == 0:
            # Дочитываем кадр
            try:
                self.frame_new[self.cur_frame_len:] = self.sourse.get_bits(self.channels[self.lvl_commut][3] - self.cur_frame_len)
                print('frame')
            except ValueError as err:
                raise ValueError(err)
        # Если есть word_tables
        else:
            # Чтение родительского кадра
            try:
                self.parent_frame = self.sourse.get_bits(self.channels[self.lvl_commut + 1][3])
            except ValueError as err:
                raise ValueError(err)
            # Выборка слов в соответствии с word_tables, то есть формирование своего кадра
            for i in range(len(self.channels[self.lvl_commut][7])):
                # В паренте от позиции до позиции + длина слова
                self.frame_new[self.cur_frame_len:self.channels[self.lvl_commut][7][i][2]] = self.parent_frame[self.channels[self.lvl_commut][7][i][1] : (self.channels[self.lvl_commut][7][i][1] + self.channels[self.lvl_commut][7][i][2])]
                self.cur_frame_len += self.channels[self.lvl_commut][7][i][2]
        if (self.frame_num % 100)  == 0:
            if self.lvl_commut == 0:
                time_ = time.clock()
                print('DMX', self.frame_num, ' frames: ', time_, 's.')

    def find_sinhr(self):
        # Чтение битовой последовательности для сравнения с синхрой
        # Длина массива в 2 раза превышает длину маркера
        try:
            value = self.sourse.get_bits(self.channels[self.lvl_commut][8][0][1]*2)
        except ValueError as err:
            raise ValueError(err)
        # Поиск синхры
        while True:
            # Проверка синхры
            if self.marker.len > 0:
                pos = value.find(self.marker)
                if len(pos) > 0:
                    self.frame_new[0:(value.len - pos[0])] = value[pos[0]:]
                    self.cur_frame_len += (value.len - pos[0])
                    return
            else:
                for i in range(len(self.used_markers)):
                    pos = value.find(self.used_markers[i][-1])
                    if len(pos) > 0:
                        self.marker = Bits(self.used_markers[i][-1])
                        print('Founded marker:', self.marker.hex)
                        self.frame_new[0:(value.len - pos[0])] = value[pos[0]:]
                        self.cur_frame_len += (value.len - pos[0])
                        return
            # Дочитываем файл
            try:
                value = value[self.channels[self.lvl_commut][8][0][1]:] + self.sourse.get_bits(self.channels[self.lvl_commut][8][0][1])
            except ValueError as err:
                raise ValueError(err)
