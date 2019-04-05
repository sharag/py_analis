#ifndef FRAMESAVER_H
#define FRAMESAVER_H

#include <QList>
#include <QString>
#include "common.h"
#include "filereader.h"

struct interval
{
    QTime intBegin;
    int posBegin;
    QTime intMiddle;
    QTime intEnd;
    int posEnd;
};


// Объекты этого класса сохраняют кадры, длина которых кратна 8 битам
class frameSaver : public QObject
{
    Q_OBJECT

public:
    frameSaver(QString fname_,
               frameParamSt frameParam_,
               fileReader *fReader_,
               QVector <sincParamSt> sincVect_,
               countParamSt countParam_);
    ~frameSaver();
    int appendFrame(QVector <sincFindRezSt*>* rezultsSinc);
    void appendFrame(frameSt frame);
    QVector <frameSt> frames;
    QString fname;
    int goalCountLen;

private:
    frameParamSt frameParam;
    fileReader *fReader;
    QVector <sincParamSt> sincVect;
    countParamSt countParam;
    QString strToLog;
    qint64 getCount(QVector <char>* vData);
    void checkCount();
    frameSt getBadFrame();
    void countRecovery(int beg, int end);
    void addInterval(frameSt* frame);
    void addFrameInInt(frameSt* frame, int numInt, int pos);
    int getNInterval(frameSt* frame);
    int findFirstMaxErr(int beg, int end);
    QList <interval>* intervals;
    float bitTime; // Время на один бит в милисекундах
    qint64 maxCountVal;

    QVector <char> data; // Массив под данные
    QVector <char> baddata; // Массив под данные
    QVector <char> tempData;

signals:
    //void sendError(QString);
    void sendStrToLog(QString);
};

#endif // FRAMESAVER_H
