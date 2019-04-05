#include "dmxthread.h"
#include "filereader.h"
#include "QList"
#include "QFileDialog"
#include "QMessageBox"
#include "QTextCursor"
#include "QPlainTextEdit"
#include "bytetobit.h"
#include "QVector"
#include "QFile"
#include "QDir"
#include "QObject"
#include "QPointer"
#include "QString"
#include "QProgressBar"
#include <QDebug>
#include "sincfinder.h"
#include "framesaver.h"
#include "common.h"
#include "logwriter.h"
#include "filewriter.h"

DMXThread::DMXThread(QStringList inFlist_,
                     QString outFname_,
                     frameParamSt frameParam_,
                     QVector <sincParamSt> sincVect_,
                     countParamSt countParam_)
{
    inFlist = inFlist_;
    outFname = outFname_;
    frameParam = frameParam_;
    sincVect = sincVect_;
    countParam = countParam_;
    // Логгер
    logWriterObj = new logWriter(outFname);
    connect(logWriterObj,
            SIGNAL(sendError(QString)),
            this,
            SLOT(needSendError(QString)));
    connect(this,
            SIGNAL(sendStrToLog(QString)),
            logWriterObj,
            SLOT(sendToLog(QString)));
    qDebug() << "DMXThread: Constructor.";
}


void DMXThread::run()
{
    qint64 progrAllVol = 0.; // Объем входных файлов
    qint64 progrCurVol = 0; // Обработанный объем
    int curPersent = 0; // Текущий процент выполнения обработки
    sincFinder * sfinder; //Указатель на поисковик синхрпокомбинаций
    fileWriter * fwriter; // указатель на записыватель файлов
    qint64 curBit = 0;
    QString fname; // Переменные для выплевывания на морды

    // Преобразование вектора параметров синхрокомбинации
    rezultsSinc = new QVector <sincFindRezSt*>; // Попутно готовим вектор для результатов
    for (int i = 0; i < sincVect.length(); i++)
    {
        QByteArray array = sincVect.at(i).sincStr.toLocal8Bit().data(); // Массив значений символов синхрокомбинации
        sincVect[i].sincVal = new QVector<char>(array.length());
        for (int j = 0; j < sincVect[i].sincVal->length(); j++) // извлечение из QByteArray в QVector<char>
            sincVect[i].sincVal->replace(j, (array.at(j) - '0'));
        sincVect[i].sincValRev = new QVector<char>(array.length());
        for (int j = 0; j < sincVect[i].sincVal->length(); j++)
            sincVect[i].sincValRev->replace(j, !(array.at(j) - '0'));
        // вектор для результатов
        sincFindRezSt* sincRez = new sincFindRezSt;
        sincRez->sincPos = 0;
        sincRez->inverseSign = false;
        sincRez->numErr = 0;
        rezultsSinc->append(sincRez);
    }

    // Рассчет общего объема входных файлов и инициализация файлочитателей кадрохранителей
    qDebug() << "DMXThread: Vollum of in files, init filereaders and filesavers: processed.";
    for (int i = 0; i < inFlist.length(); i++)
    {
        progrAllVol += qint64(QFile(inFlist.at(i)).size());
        // Создание и проверка файлочитателей
        fileReader* fileReaderObj = new fileReader(inFlist.at(i));
        if (!fileReaderObj->inF_valid)
        {
            strToLog = "DMX: Error for fileReader initialisation! ";
            strToLog += "DMX: File name:" + fileReaderObj->inFname;
            emit sendStrToLog(strToLog);
            strToLog = "Ошибка чтения файла: " + fileReaderObj->inFname +
                    ". Проверьте исходный файл.";
            emit sendError(strToLog);
            emit sendStopped(true);
            return;
        }
        inFreaders.append(fileReaderObj);
        connect(inFreaders.at(i),
                SIGNAL(sendError(QString)),
                this,
                SLOT(needSendError(QString)));
        connect(inFreaders.at(i),
                SIGNAL(sendStrToLog(QString)),
                this,
                SLOT(needSendStrToLog(QString)));
        // Создание кадрохранителей
        frameSaver* frsaver = new frameSaver(inFreaders.at(i)->inFname,
                                             frameParam,
                                             inFreaders.at(i),
                                             sincVect,
                                             countParam);
        frsavers.append(frsaver);
        connect(frsavers.at(i),
                SIGNAL(sendStrToLog(QString)),
                this,
                SLOT(needSendStrToLog(QString)));
    }

    // Восстановление структуры
    strToLog = "DMXThread: Frame structure restoring begin.";
    qDebug() << strToLog;
    emit sendStrToLog(strToLog);

    // Цикл по количеству файлов
    qint64 lastVol = 0;
    for (int i = 0; i < inFreaders.length(); i++)
    {
        // Инициализация поисковика синхрокомбинации
        sfinder = new sincFinder(sincVect,
                                 frameParam,
                                 inFreaders.at(i));
        curBit = 0;

        // Цикл по кадрам в пределах одного файла
        fname = QFileInfo(QFile(inFreaders.at(i)->inFname)).fileName();
        while((curBit + frameParam.lenFrame) < (inFreaders.at(i)->inF_size * 8))
        {
            // Поиск всех синхрокомбинаций в кадре сразу. -1 - значит не нашел или файл закончился
            if (sfinder->findNextFrame(curBit, rezultsSinc) < 0)
                break;
            // Добавление очередного кадра. -1 - значит не нашел или файл закончился
            if (frsavers.at(i)->appendFrame(rezultsSinc) < 0)
                break;
            // Сообщение наверх
            strToLog = "Файл: " + fname + ". Обнаружено кадров: ";
            strToLog += QString::number(frsavers.at(i)->frames.length()) + ".";
            emit sendNumFrames(strToLog);
            // Подведение позиционера в файле
            curBit = rezultsSinc->at(0)->sincPos + frameParam.lenFrame;
            // Проценты
            progrCurVol += inFreaders.at(i)->getLastVollumReaded();
            if ((progrCurVol*100/progrAllVol - curPersent) > 1)
            {
                curPersent = int(progrCurVol*100 / progrAllVol);
                strToLog = "Файл: " + fname + ". Обнаружено кадров: ";
                strToLog += QString::number(frsavers.at(i)->frames.length()) + ".";
                emit sendProgress(curPersent, strToLog);
            }
            // если попросили остановиться
            if (needStopSign)
            {
                strToLog = "DMXThread: Emit signal stop.";
                qDebug() << strToLog;
                emit sendStrToLog(strToLog);
                emit sendStopped(true);
                return;
            }
        }
        delete sfinder;
        lastVol += inFreaders.at(i)->inF_size;
        progrCurVol = lastVol;

        // Запись обнаруженных кадров в файл
        fwriter = new fileWriter(inFlist.at(i) + ".crt");
        connect(fwriter,
                SIGNAL(sendStrToLog(QString)),
                this,
                SLOT(needSendStrToLog(QString)));
        connect(fwriter,
                SIGNAL(sendError(QString)),
                this,
                SLOT(needSendError(QString)));
        for(int j = 0; j < frsavers.at(i)->frames.length(); j++)
            fwriter->addData(frsavers.at(i)->frames.at(j).data);
        delete fwriter;
    }

    // Если не найден ни один кадр - удаление файлочитателя и кадрохранителя
    int i = 0;
    while (i < inFreaders.length())
    {
        if (frsavers.at(i)->frames.length() == 0)
        {
            frsavers.remove(i);
            inFreaders.remove(i);
            continue;
        }
        i++;
    }
    if (frsavers.length() == 0)
        return;

    // Продолжение обработки - сборка из нескольких файлов
    if (countParam.joinFramesSign)
    {
        // Обнуление прогресс бара и вывод статуса - сборка
        strToLog = "Привязка обнаруженных кадров ко времени...";
        emit sendProgress(0, strToLog);

        // Заполнение времени для каждого кадра каждого файла
        // А также оценка временного интервала между первым и последним кадрами
        QTime minTime, maxTime;
        minTime.setHMS(23,59,59);
        maxTime.setHMS(0,0,0);
        double bitTime = double(1000)/(frameParam.freqFrame * frameParam.lenFrame); // Время на один бит
        double curTime; // Переменная для хранения текущего времени
        bool countInDetect, countOutDetect; // Признак обнаружения кадра с валидным счетчиком
        for (int i = 0; i < frsavers.length(); i++) // Цикл по файлам
        {
            countInDetect = false;
            countOutDetect = false;
            // Заполнение времени для первого кадра
            curTime = frsavers.at(i)->frames.at(0).sincPos * bitTime;
            frsavers[i]->frames.first().timeFrameS = inFreaders.at(i)->fBegTime.addMSecs(int(curTime));
            // Заполнение времени для всех остальных кадров
            for (int j = 1; j < frsavers.at(i)->frames.length(); j ++) // Цикл по кадрам
            {
                // в файле нашли начало хорошего участка (2-ой кадр с валидным счетчиком)
                if (frsavers.at(i)->frames.at(j).countValidSign &&
                       frsavers.at(i)->frames.at(j - 1).countValidSign && !countInDetect)
                {
                    countInDetect = true;
                    if (frsavers.at(i)->frames.at(j - 1).timeFrameS < minTime) // Поиск самого первого времени
                        minTime = frsavers.at(i)->frames.at(j - 1).timeFrameS;
                }
                // Если после хорошего участка обнаружен плохой конец файла
                if (countInDetect && !frsavers.at(i)->frames.at(j).countValidSign)
                {
                    countOutDetect = true;
                    if (maxTime < frsavers.at(i)->frames.at(j - 1).timeFrameS)
                        maxTime = frsavers.at(i)->frames.at(j - 1).timeFrameS;
                }
                // Заполнение времени
                if (!countInDetect || countOutDetect) // Если плохое начало или плохой конец
                {
                    curTime += (frsavers.at(i)->frames.at(j).sincPos -
                                        frsavers.at(i)->frames.at(j - 1).sincPos) * bitTime;
                    frsavers.at(i)->frames[j].timeFrameS =
                            frsavers.at(i)->frames.first().timeFrameS.addMSecs(int(curTime));
                }
                else
                {
                    curTime += frameParam.lenFrame * bitTime;
                    frsavers.at(i)->frames[j].timeFrameS =
                            frsavers.at(i)->frames.first().timeFrameS.addMSecs(int(curTime));
                }
                // если попросили остановиться
                if (needStopSign)
                {
                    strToLog = "DMXThread: Emit signal stop.";
                    qDebug() << strToLog;
                    emit sendStrToLog(strToLog);
                    emit sendStopped(true);
                    return;
                }
            }
        }

        // Проверка на временной интервал
        //(Если между первым и последним кадрами с валидными счетчиками во всех файлах > 30 минут)
        int diffTime;
        diffTime = (maxTime.hour() - minTime.hour())*60*60 +
                (maxTime.minute() - minTime.minute())*60 +
                (maxTime.second() - minTime.second());
        if (diffTime > 30*60)
        {
            strToLog = "DMXThread: DiffTime > 30 minuts. Exit.";
            qDebug() << strToLog;
            emit sendStrToLog(strToLog);
            strToLog = "Зарегистрированный интервал превышает 30 минут. Сборка произведена не будет. ";
            strToLog += "Проверьте исходные файлы.";
            emit sendError(strToLog);
            emit sendStopped(true);
            return;
        }

        // Сортировка по первой позиции с валидным счетчиком.
        // Если нет такой - удаление кадрохранителя и файлочитателя

        QTime tempTime;
        int minInd; // временный хранитель индекса
        frameSaver* tempfrsaver; // временный хранитель указателя на кадрохранитель
        // Поиск моментов времени для первых валидных кадров каждого кадрохранителя
        for (int i = 0; i < frsavers.length(); i++)
            for (int j = 0; j < frsavers.at(i)->frames.length(); j++)
                if (frsavers.at(i)->frames.at(j).countValidSign)
                    begTimes.append(frsavers.at(i)->frames.at(j).timeFrameS);
        // Сортировка
        if (frsavers.length() >=2)
        {
            for (int i = 0; i < frsavers.length() - 1; i++)
            {
                //Поиск минимального времени
                minTime = begTimes.at(i);
                minInd = i;
                for (int j = i + 1; j < frsavers.length(); j++)
                {
                    if (minTime > begTimes.at(j))
                    {
                        minTime = begTimes.at(j);
                        minInd = j;
                    }
                }
                // Проверка и замена при необходимости
                if (minInd != i)
                {
                    tempTime = begTimes.at(i);
                    begTimes.replace(i, begTimes.at(minInd));
                    begTimes.replace(minInd, tempTime);

                    tempfrsaver = frsavers.at(i);
                    frsavers.replace(i, frsavers.at(minInd));
                    frsavers.replace(minInd, tempfrsaver);
                }
            }
        }


        // Начинаем собирать только те кадры, у которых правильный счетчик
        frameSaver* outFrameSaver = new frameSaver(inFreaders.at(0)->inFname,
                                                   frameParam,
                                                   inFreaders.at(0),
                                                   sincVect,
                                                   countParam);
        connect(outFrameSaver,
                SIGNAL(sendStrToLog(QString)),
                this,
                SLOT(needSendStrToLog(QString)));
        // Для прогресса
        progrCurVol = 0;
        progrAllVol = 0;
        curPersent = 0;
        for (int i = 0; i < frsavers.length(); i++)
            progrAllVol += frsavers.at(i)->frames.length();
        // Сборка
        for (int i = 0; i < frsavers.length(); i++) // Цикл по файлам
        {
            for (int j = 0; j < frsavers.at(i)->frames.length(); j++) // Цикл по кадрам
            {
                if (frsavers.at(i)->frames.at(j).countValidSign)
                    outFrameSaver->appendFrame(frsavers.at(i)->frames.at(j));
                // если попросили остановиться
                if (needStopSign)
                {
                    strToLog = "DMXThread: Emit signal stop.";
                    qDebug() << strToLog;
                    emit sendStrToLog(strToLog);
                    emit sendStopped(true);
                    delete outFrameSaver;
                    return;
                }
                // Прогресс
                progrCurVol += 1;
                if ((progrCurVol*100/progrAllVol - curPersent) > 1)
                {
                    curPersent = int(progrCurVol*100 / progrAllVol);
                    if (curPersent == 100)
                        curPersent = 99;
                    strToLog = "Собрано кадров: " + QString::number(outFrameSaver->frames.length()) + ".";
                    emit sendProgress(curPersent, strToLog);
                }
            }
        }


        // Окончательное восстановление времени
        QTime GTSBegTime = outFrameSaver->frames.first().timeFrameS;
        double timeLine = 0;
        for (int i = 1; i < outFrameSaver->frames.length(); i++)
        {
            timeLine += frameParam.lenFrame * bitTime;
            outFrameSaver->frames[i].timeFrameS = GTSBegTime.addMSecs(int(timeLine));
        }

        // Запись собранных кадров в файл
        fwriter = new fileWriter(QFileInfo(QFile(inFreaders.at(0)->inFname)).path() + "/gts.bi1");
        connect(fwriter,
                SIGNAL(sendStrToLog(QString)),
                this,
                SLOT(needSendStrToLog(QString)));
        connect(fwriter,
                SIGNAL(sendError(QString)),
                this,
                SLOT(needSendError(QString)));
        for(int j = 0; j < outFrameSaver->frames.length(); j++)
            fwriter->addData(outFrameSaver->frames.at(j).data);
        delete fwriter;

        // Еще немного прогресса
        curPersent = 100;
        strToLog = "Собрано кадров: " + QString::number(outFrameSaver->frames.length()) + ".";
        emit sendProgress(curPersent, strToLog);


        // Запись доп файла
        // № по порядку | абсолютное время (чч:мм:сс.ссс) | относительное аремя (в мс) | качество (вероятность ошибки на бит)
        fwriter = new fileWriter(QFileInfo(QFile(inFreaders.at(0)->inFname)).path() + "/gts.info");
        connect(fwriter,
                SIGNAL(sendStrToLog(QString)),
                this,
                SLOT(needSendStrToLog(QString)));
        connect(fwriter,
                SIGNAL(sendError(QString)),
                this,
                SLOT(needSendError(QString)));

        QString nextStr;

        qint64 firstTime = outFrameSaver->frames.first().timeFrameS.hour() * 60 * 60 * 1000 +
                outFrameSaver->frames.first().timeFrameS.minute() * 60 * 1000 +
                outFrameSaver->frames.first().timeFrameS.second() * 1000 +
                outFrameSaver->frames.first().timeFrameS.msec();

        int numSincBit = 0;
        for (int j = 0; j < sincVect.length(); j++)
        {
            numSincBit += sincVect.at(j).sincStr.length();
        }

        for (int j = 0; j < outFrameSaver->frames.length(); j++)
        {
            qint64 secTime = outFrameSaver->frames.at(j).timeFrameS.hour() * 60 * 60 * 1000 +
                    outFrameSaver->frames.at(j).timeFrameS.minute() * 60 * 1000 +
                    outFrameSaver->frames.at(j).timeFrameS.second() * 1000 +
                    outFrameSaver->frames.at(j).timeFrameS.msec();
            nextStr = QString::number(j) + "\t| " +
                    QString::number(outFrameSaver->frames.at(j).timeFrameS.hour()) + ":" +
                    QString::number(outFrameSaver->frames.at(j).timeFrameS.minute()) + ":" +
                    QString::number(outFrameSaver->frames.at(j).timeFrameS.second() +
                                    double(outFrameSaver->frames.at(j).timeFrameS.msec())/1000) + "\t| " +
                    QString::number(double(secTime - firstTime)/1000) + "\t| " +
                    QString::number(getErRate(outFrameSaver,
                                              j,
                                              numSincBit,
                                              frameParam.freqFrame/10)) + '\n';
            fwriter->addData(nextStr);
        }
        delete fwriter;
        delete outFrameSaver;
    }

    // Завершение работы
    while (frsavers.length())
        frsavers.removeFirst();
    strToLog = "DMXThread: out.";
    qDebug() << strToLog;
    emit sendStrToLog(strToLog);
    emit sendStopped(true);
    return;
}

double DMXThread::getErRate(frameSaver* frSaver,
                           int ind,
                           int numSyncBit,
                           int winSize)
{
    int begWin = ind - winSize/2;
    int endWin = ind + winSize/2;
    if (begWin < 0)
        begWin = 0;
    if (endWin > (frSaver->frames.length() - 1))
        endWin = (frSaver->frames.length() - 1);

    int summEr = 0;
    for (int i = begWin; i <= endWin; i++)
        summEr += frSaver->frames.at(i).frameErRate;
    double erRate = double(summEr)/(numSyncBit * (endWin - begWin + 18));
    if (erRate > 1)
        erRate = 1;
    return erRate;
}


void DMXThread::needStop(bool)
{
    needStopSign = true;
    qDebug() << "DMXThread: needStop.";
}


void DMXThread::needSendError(QString str)
{
    qDebug() << "DMXThread: needSendError. " << str;
    emit sendError(str);
}


void DMXThread::needSendStrToLog(QString str)
{
    emit sendStrToLog(str);
}


DMXThread::~DMXThread()
{
    inFreaders.clear();
    inFreaders.squeeze();
    frsavers.clear();
    frsavers.squeeze();
    rezultsSinc->clear();
    rezultsSinc->squeeze();
    begTimes.clear();
    while (sincVect.length())
    {
        sincVect.first().sincVal->clear();
        sincVect.first().sincVal->squeeze();
        sincVect.first().sincValRev->clear();
        sincVect.first().sincValRev->squeeze();
        sincVect.takeFirst();
    }

    delete logWriterObj;

    qDebug() << "DMXThread: Destructor.";
}
