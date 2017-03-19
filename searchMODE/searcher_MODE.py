'''
Created on 13 янв. 2017 г.
@author: xail
'''
import os
from bitarray import bitarray

class Searcher_MODE(object):
    
    def __init__(self, fnames, numord, koef_delta, s_progress):
        self.s_progress = s_progress
        self.fnames = fnames
        self.numord = numord
        self.koef_delta = koef_delta
        # Проверка каталога на наличие файлов
        self.filesList = os.listdir(self.fnames[0])
        if len(self.filesList) < 1:
            raise BaseException("In the catalog a little of files.")
        
    def search(self):
        files_names = os.listdir(self.fnames[0]) # Список имен файлов
        progress = float(0)
        stepprogress = 1/len(files_names)
        # Цикл по количеству файлов
        for fileName in files_names: 
            # Формирование полного пути
            curFileName = self.fnames[0]+'/'+fileName
            data = self.read_files(curFileName)
            rez = self.get_stat(data)
            if rez:
                print(curFileName)
            # Прогресс
            progress += stepprogress
            self.s_progress.emit(int(progress*100))
                
    def get_stat(self, data):
        hist = list(int() for i in range(65536))
        for i in range(len(data))[1:]:
            if (data[i] - data[i-1]):
                hist[data[i] - data[i-1]] += 1
        maxDeltaNum = max(hist)
        max_delta_val = hist.index(maxDeltaNum)
        hist[max_delta_val] = 0
        second_max_delta_num = max(hist)
        #hist[max_delta_val] = maxDeltaNum
        if (maxDeltaNum/second_max_delta_num) < self.koef_delta:
            return False
        else:
            return True
            

    def read_files(self, curFileName):
        # Проверка на существование файла
        if os.path.exists(curFileName):
            fdata = None # Данные из файла
            numCurByte = 0 # Номер текущего байта в файле
            fsize = None # Размер файла в байтах
            try: # Открываем, читаем и закрываем файл
                fileID = open(curFileName, 'rb')
                fdata = fileID.read()
                fileID.close()
            except BaseException as err:
                print("err", err)
            fsize = len(fdata) # Размер файла в байтах
            numWord = fsize*8//self.numord # Количество слов 
            data = list()# Массив значений
            restData = bitarray() # Остаток данных от предыдущего байта
            restOrd = self.numord # Остаток разрядов до разрядности слова
            
            nullarray = bitarray(8)
            nullarray.setall(False)
            # Цикл по количеству слов
            for i in range(numWord):
                data.append(bitarray()) # Добавление ячейки в список 
                restOrd = self.numord # Остаток разрядов до разрядности слова
                #Цикл, пока не будут заполнены разряды очередного слова
                while restOrd > 0:
                    # Если еще остались данные
                    if len(restData) > 0:
                        if restOrd >= len(restData):
                            data[i] += restData
                            restOrd -= len(restData)
                            restData = bitarray()
                            continue
                        else:
                            data[i] += restData[0:0+restOrd]
                            del restData[0:0+restOrd]
                            restOrd = 0
                            break
                    else:
                        # Если осталось более 8 разрядов,
                        # то заполнение ячейки очередным байтом
                        if restOrd >= 8:
                            temp = bitarray(bin(fdata[numCurByte])[2:])
                            data[i] += (nullarray[0:8-len(temp)] + temp)
                            restOrd -= 8
                            numCurByte += 1
                            if len(data[i]) != 16 and restOrd == 0:
                                print(len(data[i]))
                            continue
                        # Если осталось меньше 8 разрядов,
                        # дополнение остатком разрядов
                        else:
                            temp = bitarray(bin(fdata[numCurByte])[2:])
                            restData = (nullarray[0:8-len(temp)] + temp)
                            numCurByte += 1
                            data[i] += restData[0:0+restOrd]
                            if len(data[i]) != 16:
                                print(len(data[i]))
                            del restData[0:0+restOrd]
                            restOrd = 0
                            break
            return data