#include "logwriter.h"
#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QTextStream>

logWriter::logWriter(QString outFile)
{

    QDir outDir(QFileInfo(QFile(outFile)).filePath().section('/',0,-2));
    logFName = outDir.path() + "/processing.log";
    logFile.setFileName(logFName);
    if (!logFile.open(QIODevice::Append))
    {
        QString strEr = "Ошибка создания файла лога.";
        emit sendError(strEr);
    }
    else
        logFile.close();
    connect(this,
            SIGNAL(needWriteToLog(bool)),
            this,
            SLOT(writeToFile()));
}


void logWriter::sendToLog(QString str)
{
    logList.append(str);
    if (logList.length() > 512)
        emit needWriteToLog(true);
    return;
}


void logWriter::writeToFile()
{
    QString strEr = "Ошибка записи файла лога.";
    if (logFile.open(QIODevice::Append))
    {
        QTextStream stream(&logFile);
        while (logList.length())
        {
            stream << logList.at(0);
            stream << "\n";
            if (stream.status() != QTextStream::Ok)
                emit sendError(strEr);
            logList.removeAt(0);
        }
        logFile.flush();
        logFile.close();
        return;
    }
    else
    {
        while (logList.length())
            logList.removeAt(0);
        emit sendError(strEr);
        return;
    }
}


logWriter::~logWriter()
{
    writeToFile();
    logList.clear();
}


