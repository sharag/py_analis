#ifndef DMXTHREAD_H
#define DMXTHREAD_H
#include "QThread"
#include "QString"
#include "QFileDialog"
#include "QVector"
#include "common.h"
#include "filereader.h"
#include "logwriter.h"
#include "framesaver.h"

class DMXThread : public QThread
{
    Q_OBJECT

public:
    DMXThread(QStringList inFlist_,
              QString outFname_,
              frameParamSt frameParam_,
              QList <sincParamSt> sincVect_,
              countParamSt countParam_);
    void run();
    ~DMXThread();

public slots:
    void needStop(bool);
    void needSendError(QString);
    void needSendStrToLog(QString);

private:
    QStringList inFlist;
    QString outFname, strToLog;
    QList <sincParamSt> sincVect;
    countParamSt countParam;
    frameParamSt frameParam;
    bool needStopSign = false;
    QList <sincFindRezSt*> rezultsSinc;
    QList <fileReader*> inFreaders; // Массив указателей на файлочитатели (Нужно инициализировать сразу, чтобы выявить траблы с файлами)
    QList <frameSaver*> frsavers; // Массив указателей на кадрохранители
    logWriter* logWriterObj;
    double getErRate(frameSaver* frSaver,
                     int ind,
                     int numSyncBit,
                     int winSize);
    QList<QTime> begTimes;

signals:
    void sendProgress(int,
                      QString);
    void sendNumFrames(QString);
    void sendError(QString);
    void sendStopped(bool);
    void sendStrToLog(QString);
};
namespace Ui {
class MainWindow;
}

#endif // DMXTHREAD_H
