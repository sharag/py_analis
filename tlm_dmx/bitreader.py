import sys, os
from bitstring import Bits, BitArray
import _thread_dmx
import time

class Bitreader:
    def __init__(self, f, rev):
        self.in_fname = f
        try:
            self.in_fid = open(self.in_fname, mode='rb')
            self.fsize_1proc = os.path.getsize(self.in_fname)//100
        except BaseException as err:
            raise ValueError(err)
        self.cur_fpos = 0
        self.revers = rev
        self.accum = Bits(uint=0, length=8)
        self.bcount = 0
        self.bitnum = 0
        self.byteorder = sys.byteorder
        self.revtab = self.revers_bit()  # В зависимости от логического значения self.revers формируется таблица
        # строк либо с реверсивными значениями байт при True, либо с прямым следованием бит при False

    def read_bit(self):
        if self.bcount == 0:
            try:
                r_byte = self.in_fid.read(1)
            except BaseException as err:
                raise ValueError(err)
            self.cur_fpos += 1
            if (self.cur_fpos % self.fsize_1proc) == 0:
                _thread_dmx.progr = self.cur_fpos // self.fsize_1proc
            if r_byte != b'':
                self.accum = self.revtab[r_byte[0]]
            else:
                return ''
            self.bcount = 8
        b_str = self.accum[8 - self.bcount]
        self.bcount -= 1
        return b_str

    def get_bits(self, n):
        print('bitreader in get_bits', time.clock())
        value = BitArray(length=n)
        while n > 0:
            if n >= 8 and self.bcount == 0:
                try:
                    r_byte = self.in_fid.read(1)
                except BaseException as err:
                    raise ValueError(err)
                self.cur_fpos += 1
                if (self.cur_fpos % self.fsize_1proc) == 0:
                    _thread_dmx.progr = self.cur_fpos // self.fsize_1proc
                if r_byte != b'':
                    value[(value.len - n):(value.len - n + 8)] = self.revtab[r_byte[0]]
                    self.bitnum += 8
                    n -= 8
                else:
                    raise ValueError("EOF")
            else:
                b_str = self.read_bit()
                if b_str != '':
                    value[value.len - n] = b_str
                    self.bitnum += 1
                    n -= 1
                else:
                    raise ValueError("EOF")
        print('bitreader out get_bits', time.clock())
        return value

# Формирование таблицы для реверса считанных байт
# Возвращает таблицу с массивами бит для реверса
# 0b10000000 - 0b00000001
    def revers_bit(self):
        tab = []
        if self.revers:
            for value in range(256):
                result = 0
                for i in range(8):
                    if (value >> i) & 1:
                        result |= 1 << (8 - 1 - i)
                tab.append(Bits(uint=result, length=8))
        else:
            for value in range(256):
                tab.append(Bits(uint=value, length=8))
        return tab
