#include "filereader.h"
#include "QFileDialog"
#include "QMessageBox"
#include "QTextCursor"
#include "QPlainTextEdit"
#include "QTextCursor"
#include "QIODevice"
#include "bytetobit.h"
#include "QVector"
#include "QFile"
#include "QString"
#include "QDir"
#include "QMessageBox"
#include "dmxthread.h"
#include "QDebug"
#include "QDataStream"
#include "malloc.h"


/*void reverse_bits(byte *src, unsigned int num_bytes)
{
    for(unsigned int i=0;i<num_bytes;i++)
    {
        src[i] = ((src[i] * 0x80200802ULL) & 0x0884422110ULL) * 0x0101010101ULL >> 32;
    }
}*/


fileReader::fileReader(QString inFile_)
{
    inFname = inFile_; // Объект
    posEndBit = 0; // Позиция последнего прочитанного бита в буффере
    posBegBit = 0; // Позиция первого прочитанного бита в буффере
    curReadVol = 0; // Количество прочитанных байт
    lastReadVol = 0; // Количество прочитанных байт, которые были отданы в последнем вызове getLastReadedDataVollum
    volOfBuff = int(pow(2, 20)); // Объем считываемых данных в байтах
    backOffset = int(pow(2, 14)); // Смещение назад от заданной позиции
    inF_valid = true;// Признак существования файла
    strToLog = "fileReader: fileReader object is initialising:" + inFname;
    qDebug() << strToLog;
    emit sendStrToLog(strToLog);
    // Проверка существования файла
    inQFile.setFileName(inFname);
    if (!inQFile.exists())
    {
        inF_valid = false;
        strToLog = "Файл: " + inFname + " не существует!";
        emit sendError(strToLog);
        return;
    }
    strToLog = "\n\n\nfileReader: Open file:" + inFname + ".";
    emit sendStrToLog(strToLog);

    // Определение размера файла
    inF_size = int(inQFile.size());
    if (inF_size < 1024)
    {
        strToLog = "Файл: " + inFname + " слишком короткий!";
        emit sendError(strToLog);
        inF_valid = false;
        return;
    }

    // Определение времени начала регистрации
    int hour_, min_, sek_ = 0;
    strToLog = "Файл: " + inFname + " имеет некорректное имя! Повторите выбор файлов ГТС!";
    if (QFileInfo(QFile(inFname)).fileName().split('.').length() == 2)
    {
        if (QFileInfo(QFile(inFname)).fileName().split('.').at(0).split('_').length() == 3)
        {
            try
            {
                hour_ = QFileInfo(QFile(inFname)).fileName().split('.').at(0).split('_').at(0).toInt();
                min_ = QFileInfo(QFile(inFname)).fileName().split('.').at(0).split('_').at(1).toInt();
                sek_ = QFileInfo(QFile(inFname)).fileName().split('.').at(0).split('_').at(2).toInt();
            }
            catch (...)
            {
                emit sendError(strToLog);
                inF_valid = false;
                return;
            }
        }
        else
        {
            emit sendError(strToLog);
            inF_valid = false;
            return;
        }
    }
    else
    {
        emit sendError(strToLog);
        inF_valid = false;
        return;
    }
    if (hour_ < 0 || hour_ > 23 || min_ < 0 || min_ > 60 || sek_ < 0 || sek_ > 60 )
    {
        emit sendError(strToLog);
        inF_valid = false;
        return;
    }
    else
        fBegTime.setHMS(hour_,
                        min_,
                        sek_);
}


QVector<char> fileReader::getBits(qint64 posBit,
                                  qint64 lenBit)
{
    QVector<char> outBuff;

    // Проверить, запрошенная длина превышает размер буффера
    // или запрашиваются биты вне файла
    if (lenBit >= volOfBuff*8 || (posBit + lenBit) > (inF_size*8))
    {
        strToLog = "fileReader: EOF " + inFname + ".";
        qDebug() << strToLog;
        emit sendStrToLog(strToLog);
        return outBuff;
    }
    // Проверить все ли биты попали в диапазон posBegBit posEndBit
    // если нет - перечитать буффер
    if (posBit < posBegBit || (posBit + lenBit) > posEndBit)
    {
        int offset;
        // Рассчет смещения в файле
        if (posBit > backOffset)
            offset = int((posBit - backOffset)/8);
        else
            offset = int(posBit/8);
        // Читаем
        if(!fileReaderRead(offset))
        {
            strToLog = "Ошибка чтения файла: " + inFname + "!";
            emit sendError(strToLog);
            strToLog = "fileReader: Read file error: " + inFname;
            emit sendStrToLog(strToLog);
            qDebug() << strToLog;
            return outBuff;
        }
    }
    // Вырезаем требуемый кусок из буффера и отдаем
    outBuff = curBuff.mid(int(posBit - posBegBit),
                          int(lenBit));
    return outBuff;
}


int fileReader::fileReaderRead(int beginByte)
{
    // Количество байт, которые следует прочитать
    int numByte;

    // Проверить, не превышает ли volOfBuff оставшегося объема после beginByte
    if (volOfBuff > (inF_size - beginByte))
        numByte = inF_size - beginByte;
    else
        numByte = volOfBuff;

    // Открытие файла. Если нет - возврат пустого массива
    if (!inQFile.open(QIODevice::ReadOnly))
    {
        strToLog = "Ошибка обращения к файлу: " + inFname + "!";
        emit sendError(strToLog);
        strToLog = "fileReader: File do not opened :" + inFname;
        qDebug() << strToLog;
        return 0;
    }

    // установка указателя в файле и чтение байтов
    QVector<char>* rawBytes;
    rawBytes = new QVector<char>(numByte);
    inQFile.seek(beginByte);
    inQFile.read(rawBytes->data(),
                 numByte);
    inQFile.close();

    // Преобразование в биты
    if (curBuff.length())
    {
        curBuff.clear();
        curBuff.squeeze();
    }

        //free(&curBuff);
        //delete [] &curBuff[0];
    curBuff = byteToBit(*rawBytes);
    delete rawBytes;
    posBegBit = beginByte * 8;
    posEndBit = beginByte * 8 + numByte * 8;

    // Сохранение информации о количестве прочитанных байт
    curReadVol = (beginByte + numByte);

    return -1;
}


/*Возвращает объем считанных из файла данных после последнего запроса*/
qint64 fileReader::getLastVollumReaded()
{
    qint64 outValue = curReadVol - lastReadVol;
    if (outValue > 0)
    {
        lastReadVol = curReadVol;
        return outValue;
    }
    else
        return 0;
}


fileReader::~fileReader()
{
    curBuff.clear();
    curBuff.squeeze();
    qDebug() << "fileReader: fileReader object is destroed.";
    qDebug() << "fileReader: File name is :" << inFname;
}
