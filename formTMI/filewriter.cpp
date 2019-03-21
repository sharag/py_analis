#include "filewriter.h"
#include "filereader.h"
#include "QFileDialog"
#include "dmxthread.h"
#include "QMessageBox"
#include "QTextCursor"
#include "QPlainTextEdit"
#include "bytetobit.h"
#include "QVector"
#include "QFile"
#include "QPointer"
#include "QDir"
#include "QtDebug"

fileWriter::fileWriter(QString outF_name)
{
    volBuff = 1024*8; // Максимальный объем буффера
    outFile.setFileName(outF_name);// Объект - файл
    if (outFile.exists())
        outFile.remove();
    curBuff = new QVector<char>;// Буффер
    strToLog = "fileWriter: Constructor. Out file: " + outF_name;
    qDebug() << strToLog;
    emit sendStrToLog(strToLog);
}


void fileWriter::addData(QString CurStr)
{
    //const char * ptrStr = CurStr.toLocal8Bit().constData();
    QVector<char> data;
    for (int i = 0; i < CurStr.length(); i++)
        data.append(CurStr.at(i).cell());
        //data.append(*(ptrStr + i));

    if (!data.length())
        return;
    int lenData = data.length();
    int avlblVolBuf = volBuff - curBuff->length();
    int numByteToAdd = 0;
    if (lenData < avlblVolBuf)
        numByteToAdd = lenData;
    else
        numByteToAdd = avlblVolBuf;

    curBuff->append(data.mid(0, numByteToAdd));
    data.remove(0, numByteToAdd);
    if (curBuff->length() == volBuff)
        writeToFile();
    if (data.length())
        addData(data);
}


void fileWriter::addData(QVector<char> data)
{

    if (!data.length())
        return;
    int lenData = data.length();
    int avlblVolBuf = volBuff - curBuff->length();
    int numByteToAdd = 0;
    if (lenData < avlblVolBuf)
        numByteToAdd = lenData;
    else
        numByteToAdd = avlblVolBuf;

    curBuff->append(data.mid(0, numByteToAdd));
    data.remove(0, numByteToAdd);
    if (curBuff->length() == volBuff)
        writeToFile();
    if (data.length())
        addData(data);
}


void fileWriter::writeToFile()
{
    if(outFile.open(QIODevice::Append))
    {
        QDataStream stream(&outFile);
        if (stream.writeRawData(curBuff->data(), curBuff->length()) != curBuff->length())
        {
            strToLog = "Ошибка записи в файл: " + outFile.fileName() + ".";
            emit sendError(strToLog);
            strToLog = "fileWriter: Error write file: " + outFile.fileName();
            emit sendStrToLog(strToLog);
        }
        curBuff->~QVector();
        curBuff = new QVector<char>;
    }
    else
    {
        strToLog = "Ошибка записи в файл: " + outFile.fileName() + ".";
        emit sendError(strToLog);
    }
    outFile.close();
}


fileWriter::~fileWriter()
{
    writeToFile();
    strToLog = "fileWriter: Save data to file!";
    qDebug() << strToLog;
    emit sendStrToLog(strToLog);
    strToLog = "fileWriter: Destructor.";
    qDebug() << strToLog;
}
