#ifndef FILEREADER_H
#define FILEREADER_H

#include <QObject>
#include <QString>
#include <QFileDialog>
#include <QFile>
#include <QTime>

class fileReader : public QObject
{
    Q_OBJECT

public:
    fileReader(QString inFile_);
    ~fileReader();
    QVector<char>* getBits(qint64 posBit,
                           qint64 lenBit);
    qint64 getLastVollumReaded();
    bool inF_valid;
    int inF_size;
    QString inFname;
    QTime fBegTime;


private:
    int fileReaderRead(int beginByte);
    int volOfBuff; // Объем считываемых данных в байтах
    int backOffset; // Смещение назад от заданной позиции
    QFile inQFile;
    qint64 posEndBit;
    qint64 posBegBit;
    QVector<char> curBuff;
    QVector<char> rawBytes;
    QVector<char> outBuff;
    qint64 lastReadVol;
    qint64 curReadVol;
    QString strToLog;

signals:
    void sendError(QString);
    void sendStrToLog(QString);
};

namespace Ui {
class MainWindow;
}


#endif // FILEREADER_H
