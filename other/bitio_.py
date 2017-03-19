import sys

def reversBit(value):
# Производится реверс байта. На вход - 1 байт! типа int
    result = 0
    for i in range(8):
        if (value >> i) & 1:
            result |= 1 << (8 - 1 - i)
    return result

class BitWriter:
    def __init__(self, f):
        self.accumulator = 0
        self.bcount = 0
        self.out = f
 
    def __del__(self):
        try:
            self.flush()
        except ValueError:  # I/O operation on closed file
            pass
 
    def writebit(self, bit):
        if self.bcount == 8 :
            self.flush()
        if bit > 0:
            self.accumulator |= (1 << (7-self.bcount))
        self.bcount += 1
 
    def writebits(self, bits, n):
        while n > 0:
            self.writebit( bits & (1 << (n-1)) )
            n -= 1
 
    def flush(self):
        self.out.write(chr(self.accumulator))
        self.accumulator = 0
        self.bcount = 0
 
 
class BitReader:
    def __init__(self, f, rev):
        self.input = f
        self.accumulator = 0
        self.bcount = 0
        self.read = 0
        self.revers = rev

    def readbit(self):
        if self.bcount == 0 :
            a = int.from_bytes(self.input.read(1), sys.byteorder)
            if self.revers:
                 a = reversBit(a)
            self.accumulator = a
            self.bcount = 8
            self.read = 1
        rv = ( self.accumulator & ( 1 << (self.bcount-1) ) ) >> (self.bcount-1)
        self.bcount -= 1
        return rv
 
    def readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit()
            n -= 1
        return v
