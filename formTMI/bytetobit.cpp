#include "bytetobit.h"


void byteToBit(char * bytesIn,
               qint64 bytesInCount,
               char * bitsOut)
{
    for (qint64 i = 0; i < bytesInCount; i++)
    {
        for (int j = 0; j < 8; j++)
            bitsOut[i*8+j] = ((bytesIn[i]>>j) & 1) ? 1 : 0;
    }
}

void bitToByte(char * bitsIn,
               qint64 bitsInCount,
               char * bytesOut)
{
   for (qint64 i = 0; i < bitsInCount/8; i++)
   {
       bytesOut[i] = ( (bitsIn[i*8+0] << 0) |
                       (bitsIn[i*8+1] << 1) |
                       (bitsIn[i*8+2] << 2) |
                       (bitsIn[i*8+3] << 3) |
                       (bitsIn[i*8+4] << 4) |
                       (bitsIn[i*8+5] << 5) |
                       (bitsIn[i*8+6] << 6) |
                       (bitsIn[i*8+7] << 7)  );
   }
}


QVector<char> byteToBit(QVector<char> &bytes)
{
    QVector<char> bits(bytes.size()*8);
    for (int i = 0; i < bytes.size(); i++)
    {
        for (int j = 0; j < 8; j++)
            bits[i*8+j] = ((bytes[i]>>j) & 1) ? 1 : 0;
    }
    return bits;
}

QVector<char> bitToByte(QVector<char> &bits)
{
    QVector<char> bytes(bits.size()/8);
    for (int i = 0; i < bytes.size(); i++)
    {
        bytes[i] = ( (bits[i*8+0] << 0) |
                     (bits[i*8+1] << 1) |
                     (bits[i*8+2] << 2) |
                     (bits[i*8+3] << 3) |
                     (bits[i*8+4] << 4) |
                     (bits[i*8+5] << 5) |
                     (bits[i*8+6] << 6) |
                     (bits[i*8+7] << 7)  );
    }
    return bytes;
}
