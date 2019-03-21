#include "framesaver.h"
#include "bytetobit.h"
#include "QDebug"
#include "math.h"


frameSaver::frameSaver(QString fname_,
                       frameParamSt frameParam_,
                       fileReader *fReader_,
                       QVector <sincParamSt> sincVect_,
                       countParamSt countParam_)
{
    fname = fname_;
    frameParam = frameParam_;
    fReader = fReader_;
    sincVect = sincVect_;
    countParam = countParam_;
    goalCountLen = 0;
    if (countParam.countLen <= 8)
        goalCountLen = 8;
    else if (countParam.countLen <= 16)
        goalCountLen = 16;
    else if (countParam.countLen <= 32)
        goalCountLen = 32;
    else if (countParam.countLen <= 64)
        goalCountLen = 64;
    intervals = new QList <interval>;
    bitTime = float(1000)/(frameParam.freqFrame * frameParam.lenFrame); // Время на один бит в мс
    maxCountVal = int(pow(2, countParam.countLen)) - 1;
}


void frameSaver::appendFrame(frameSt* frame)
{
    frameSt* badFrame;
    int curPos;
    QTime tempTime;
    float timeDiffMS = 0;
    int curNumInt = getNInterval(frame); // Номер интервала, которому принадлежит кадр

    if (intervals->at(curNumInt).posBegin < 0)
    { // Если в этом интервале нет еще кадров
        if (curNumInt == 0)
        {// Если это первый интервал
            addFrameInInt(frame,
                          curNumInt,
                          0); // Добавляем сразу
            return;
        }
        else
        {// Если это не первый интервал (это же означает, что кадры во frames уже есть)
            // Оценка времени между текущим и предыдущим интервалами
            float diffInt = intervals->at(curNumInt).intBegin.hour()*60*60*1000 +
                    intervals->at(curNumInt).intBegin.minute()*60*1000 +
                    intervals->at(curNumInt).intBegin.second()*1000 +
                    intervals->at(curNumInt).intBegin.msec() -
                    intervals->at(curNumInt - 1).intEnd.hour()*60*60*1000 -
                    intervals->at(curNumInt - 1).intEnd.minute()*60*1000 -
                    intervals->at(curNumInt - 1).intEnd.second()*1000 -
                    intervals->at(curNumInt - 1).intEnd.msec();
            diffInt = diffInt/(bitTime*frameParam.lenFrame*maxCountVal);

            tempTime = frames.last()->timeFrameS;

            // Вставка BAD кадров до конца предыдущего интервала
            curPos = frames.length() - 1;
            while (frames.at(curPos)->frameCNT < maxCountVal)
            {
                timeDiffMS = timeDiffMS + frameParam.lenFrame*bitTime;
                badFrame = getBadFrame();
                badFrame->frameCNT = frames.last()->frameCNT + 1;
                badFrame->frameErRate = int(pow(2, 16));
                badFrame->countValidSign = true;
                badFrame->timeFrameS.setHMS(tempTime.hour(),
                                            tempTime.minute(),
                                            tempTime.second(),
                                            tempTime.msec());
                badFrame->timeFrameS = badFrame->timeFrameS.addMSecs(int(timeDiffMS));
                addFrameInInt(badFrame,
                              getNInterval(badFrame),
                              curPos + 1);
                curPos = frames.length() - 1;
            }

            // Вставка пропущенных интервалов
            while (roundf(diffInt) >= float(0.8))
            {
                for (int i = 0; i < maxCountVal; i++)
                {
                    timeDiffMS = timeDiffMS + frameParam.lenFrame*bitTime;
                    badFrame = getBadFrame();
                    badFrame->frameCNT = i;
                    badFrame->frameErRate = int(pow(2, 16));
                    badFrame->countValidSign = true;
                    badFrame->timeFrameS.setHMS(tempTime.hour(),
                                                tempTime.minute(),
                                                tempTime.second(),
                                                tempTime.msec());
                    badFrame->timeFrameS = badFrame->timeFrameS.addMSecs(int(timeDiffMS));
                    addFrameInInt(badFrame,
                                  getNInterval(badFrame),
                                  curPos + 1);
                    curPos = frames.length() - 1;
                }
                diffInt -= 1;
            }
        }
    }
    else
    { // Это не первый кадр в интервале
        // Поиск кадра с таким же номером
        for (int i = intervals->at(curNumInt).posBegin; i <= intervals->at(curNumInt).posEnd; i++)
            if (frames.at(i)->frameCNT == frame->frameCNT)
            {
                // Если в новом кадре меньше ошибок - замена кадра
                if (frames.at(i)->frameErRate > frame->frameErRate)
                {
                    frames.replace(i, frame);
                    strToLog = "Finded repeated frame: first frame: count " +
                            QString::number(frames.at(i)->frameCNT) + ", number of error " +
                            QString::number(frames.at(i)->frameErRate) +
                            "; second frame: count " + QString::number(frame->frameCNT) +
                             + ", number of error " + QString::number(frame->frameErRate);
                    qDebug() << strToLog;
                    emit sendStrToLog(strToLog);
                }
                return;
            }
    }

    // Если нет такого же кадра (и это не первый кадр)
    // Добавление BAD кадров до целевого
    qint64 startCount = 0;
    if (frames.last()->frameCNT == maxCountVal)
        startCount = 0;
    else
        startCount = frames.last()->frameCNT + 1;

    tempTime = frames.last()->timeFrameS;
    timeDiffMS = 0;
    while (startCount < frame->frameCNT)
    {
        timeDiffMS = timeDiffMS + frameParam.lenFrame*bitTime;
        badFrame = getBadFrame();
        badFrame->frameCNT = startCount;
        badFrame->frameErRate = int(pow(2, 16));
        badFrame->countValidSign = true;
        badFrame->timeFrameS.setHMS(tempTime.hour(),
                                    tempTime.minute(),
                                    tempTime.second(),
                                    tempTime.msec());
        badFrame->timeFrameS = badFrame->timeFrameS.addMSecs(int(timeDiffMS));
        addFrameInInt(badFrame,
                      getNInterval(badFrame),
                      (frames.length() - 1));
        startCount ++;
    }

    // Добавление целевого кадра
    addFrameInInt(frame, getNInterval(frame), frames.length());
    return;
}


/*Функция вынесена отдельно, так как в ней при добавлении кадра
 * осуществляется сдвиг позиций всех последующих интервалов*/
void frameSaver::addFrameInInt(frameSt* frame, int numInt, int pos)
{
    strToLog = "pos: " + QString::number(pos) + ", frameCNT: " + QString::number(frame->frameCNT) +
            ", time: " + frame->timeFrameS.toString();
    qDebug() << strToLog;
    emit sendStrToLog(strToLog);
    frames.insert(pos, frame);
    interval curInt;
    if (intervals->at(numInt).posBegin < 0) // если этому интервалу не соответсвует ни один кадр
    {
        curInt = intervals->at(numInt);
        curInt.posBegin = pos;
        curInt.posEnd = pos;
        intervals->replace(numInt, curInt);
    }
    else
    {
        // Смещение последней позиции текущего интервала
        curInt = intervals->at(numInt);
        curInt.posEnd = curInt.posEnd + 1;
        intervals->replace(numInt, curInt);
        // Смещение всех позиций последующих интервалов
        for (int i = numInt + 1; i < intervals->length(); i++)
        {
            curInt = intervals->at(i);
            if (curInt.posBegin < 0)
                continue;
            curInt.posBegin = curInt.posBegin + 1;
            curInt.posEnd = curInt.posEnd + 1;
            intervals->replace(i, curInt);
        }
    }
}


int frameSaver::getNInterval(frameSt* frame)
{
    // Доверительный интервал в милисекундах
    int diffInt = int(frameParam.lenFrame *
                      pow(2, countParam.countLen) *
                      (frameParam.offsetSincFail/100.) *
                      double(bitTime));
    for (int i = 0; i < intervals->length(); i++)
    {
        // Проверка на попадание в интервал с учетом доверительного интервала
        if (frame->timeFrameS > intervals->at(i).intBegin.addMSecs(-diffInt) &&
                frame->timeFrameS < intervals->at(i).intEnd.addMSecs(diffInt))
        {
            // Проверка на позицию
            if ((frame->frameCNT < maxCountVal/3) && // если счетчик в первой трети
                    (frame->timeFrameS > intervals->at(i).intMiddle)) // а время во второй половине
                continue;
            else if ((frame->frameCNT > (maxCountVal - maxCountVal/3)) && // если счетчик в третьей трети
                     (frame->timeFrameS < intervals->at(i).intMiddle)) // а время в первой половине
                continue;
            // проверки на интервал с учетом доверительного интервала и на позицию пройдены
            return i;
        }
    }
    // если не попал - добавить интервал и вернуть его номер
    addInterval(frame);
    return getNInterval(frame);
}


void frameSaver::addInterval(frameSt* frame)
{
    interval newInt;
    newInt.posBegin = -1;
    newInt.posEnd = -1;
    if (frame->frameCNT == 0)
        newInt.intBegin = frame->timeFrameS;
    else
        newInt.intBegin = frame->timeFrameS.addMSecs(-int(bitTime*frameParam.lenFrame*frame->frameCNT));
    if (frame->frameCNT == maxCountVal)
        newInt.intEnd = frame->timeFrameS;
    else
        newInt.intEnd = frame->timeFrameS.addMSecs(int(bitTime*frameParam.lenFrame*
                                                       (maxCountVal - frame->frameCNT + 1)));
    // Рассчет середины
    int begMS = newInt.intBegin.hour()*60*60*1000 +
            newInt.intBegin.minute()*60*1000 +
            newInt.intBegin.second()*1000 +
            newInt.intBegin.msec();
    int endMS = newInt.intEnd.hour()*60*60*1000 +
            newInt.intEnd.minute()*60*1000 +
            newInt.intEnd.second()*1000 +
            newInt.intEnd.msec();
    newInt.intMiddle = newInt.intBegin.addMSecs((endMS - begMS)/2);
    // Определение позиции интервала и его добавление
    if (intervals->length())
        for (int i = 0; i < intervals->length(); i++)
            if (newInt.intBegin < intervals->at(i).intBegin) // Если интервал не последний
            {
                //newInt.posBegin = intervals->at(i).posBegin;
                //newInt.posEnd = intervals->at(i).posBegin;
                intervals->insert(i, newInt);
                return;
            }
    // Если интервал последний, но не первый
    //if (intervals->length() > 0)
    //{
    //    newInt.posBegin = intervals->last().posEnd + 1;
    //    newInt.posEnd = intervals->last().posEnd + 1;
    //}
    intervals->append(newInt);
    return;
}


int frameSaver::appendFrame(QVector <sincFindRezSt*>* rezultsSinc)
{
    frameSt *newFrame = new frameSt;
    QList <char> * data; // Массив под данные
    data = new QList <char>;
    qint64 bufLen;
    qint64 curBitPos = 0;
    int numEr = 0;

    // Цикл по синхрокомбинациям
    for (int i = 0; i < sincVect.length(); i++)
    {
        // Добавляем синхру
        data->append(sincVect.at(i).sincVal->toList());
        // Добавляем данные
        curBitPos = rezultsSinc->at(i)->sincPos + sincVect.at(i).sincVal->length();
        if ((sincVect.length() - i) > 1)
            bufLen = sincVect.at(i + 1).sincPos -
                    sincVect.at(i).sincPos -
                    sincVect.at(i).sincVal->length();
        else
            bufLen = frameParam.lenFrame -
                    sincVect.at(i).sincPos -
                    sincVect.at(i).sincVal->length();
        QList <char> tempData = fReader->getBits(curBitPos,
                                                 bufLen).toList();
        if (tempData.length() != bufLen)
            return -1;
        if (rezultsSinc->at(i)->inverseSign)
            for (int j = 0; j < tempData.length(); j++)
                tempData.replace(j, !tempData.at(j));
        data->append(tempData);
        // Добавляем ошибки
        numEr += rezultsSinc->at(i)->numErr;
    }
    // Заполнение кадра
    QVector <char> vData = data->toVector();
    if (countParam.joinFramesSign)
        newFrame->frameCNT = getCount(&vData);
    else
        newFrame->frameCNT = -1;
    newFrame->data = bitToByte(vData);
    newFrame->frameErRate = numEr;
    newFrame->sincPos = rezultsSinc->at(0)->sincPos;
    newFrame->countValidSign = false;
    newFrame->timeFrameS.setHMS(0,0,0);
    delete data;
    delete [] &vData[0];

    // Проверка на длину кадра
    int numFr4add = 0;
    // Примерное вычисление количества добавляемых кадров
    if (!frames.length()) // Если кадр первый, сразу записываем
    {
        frames.append(newFrame);
        strToLog = "frameSaver: Frame:\t" + QString::number(frames.length()) +
                "\tSinc pos:\t" + QString::number(newFrame->sincPos) +
                "\tDelta:\t" + QString::number((newFrame->sincPos-frames.last()->sincPos)) +
                "\tNumErr:\t" + QString::number(newFrame->frameErRate) +
                "\tframeCNT:\t" + QString::number(newFrame->frameCNT);
        qDebug() << strToLog;
        emit sendStrToLog(strToLog);
        return frames.length();
    }
    else // Если нет - считаем разность между позициями синхрокомбинаций
        numFr4add = int(roundf(float(newFrame->sincPos-frames.last()->sincPos)/frameParam.lenFrame));


    // Оценка приращения
    if (numFr4add == 1) // Если между позициями синхрокомбинаций один кадр
    {
        strToLog = "frameSaver: Frame:\t" + QString::number(frames.length()) +
                "\tSinc pos:\t" + QString::number(newFrame->sincPos) +
                "\tDelta:\t" + QString::number((newFrame->sincPos-frames.last()->sincPos)) +
                "\tNumErr:\t" + QString::number(newFrame->frameErRate) +
                "\tframeCNT:\t" + QString::number(newFrame->frameCNT);
        qDebug() << strToLog;
        emit sendStrToLog(strToLog);
        frames.append(newFrame);
        if (countParam.joinFramesSign)
            checkCount();
        return frames.length();
    }
    else if (numFr4add < 1) // Если существенно меньше кадра (невыполнимая ветка)
    {
        strToLog = "frameSaver: Frame not added. Frame:\t" + QString::number(frames.length());
        strToLog += "\tSinc pos:\t" + QString::number(newFrame->sincPos);
        strToLog += "\tDelta:\t" + QString::number((newFrame->sincPos-frames.last()->sincPos));
        strToLog += "\tNumErr:\t" + QString::number(newFrame->frameErRate);
        strToLog += "\tframeCNT\t:" + QString::number(newFrame->frameCNT);
        qDebug() << strToLog;
        emit sendStrToLog(strToLog);
        return frames.length();
    }
    else // Если между позициями синхрокомбинаций две длины кадра и более
    {
        // Добавляем пропущенные кадры с нулевым заполнением
        for (int i = 0; i < (numFr4add - 1); i++)// Цикл по количеству пропущенных кадров
            // Добавление кадра
            frames.append(getBadFrame());
        strToLog = "frameSaver: Added " + QString::number(numFr4add - 1) + " bad frames!!!";
        qDebug() << strToLog;
        emit sendStrToLog(strToLog);

        strToLog = "frameSaver: Frame:\t" + QString::number(frames.length());
        strToLog += "\tSinc pos:\t" + QString::number(newFrame->sincPos);
        strToLog += "\tDelta:\t" + QString::number((newFrame->sincPos-frames.last()->sincPos));
        strToLog += "\tNumErr:\t" + QString::number(newFrame->frameErRate);
        strToLog += "\tframeCNT:\t" + QString::number(newFrame->frameCNT);
        qDebug() << strToLog;
        emit sendStrToLog(strToLog);
        frames.append(newFrame);
        return frames.length();
    }
}


qint64 frameSaver::getCount(QVector <char>* vData)
{
    qint64 countVal = 0; // Инициализация первичного значения счетчика
    QVector <char> countChar = vData->mid(countParam.countPos, countParam.countLen);
    if (goalCountLen != countParam.countLen)
        for (int i = 0; i < (goalCountLen - countParam.countLen); i++)
            countChar.append(0);
    // Цикл по разрядам для получения значения счетчика
    qint64 begMask = 1;
    for (int i = 0; i < goalCountLen; i++)
        if (countChar.at(goalCountLen - i - 1))
            countVal |= (begMask << i);
    return countVal;
}


/*Добавление кадра с восстановленными синхрокомбинациями и нулевым заполнением*/
frameSt * frameSaver::getBadFrame()
{
    frameSt *badFrame; // Вставляемый кадр
    QList <char>* baddata; // Массив под данные
    badFrame = new frameSt;
    baddata = new QList <char>;
    qint64 bufLen;
    // Цикл по синхрокомбинациям
    for (int i = 0; i < sincVect.length(); i++)
    {
        if ((sincVect.length() - i) > 1)
            bufLen = sincVect.at(i + 1).sincPos -
                    sincVect.at(i).sincPos -
                    sincVect.at(i).sincVal->length();
        else
            bufLen = frameParam.lenFrame -
                    sincVect.at(i).sincPos -
                    sincVect.at(i).sincVal->length();
        // Добавляем синхру
        baddata->append(sincVect.at(i).sincVal->toList());
        if ((sincVect.length() - i) > 1)
            bufLen = sincVect.at(i + 1).sincPos -
                    sincVect.at(i).sincPos -
                    sincVect.at(i).sincVal->length();
        else
            bufLen = frameParam.lenFrame -
                    sincVect.at(i).sincPos -
                    sincVect.at(i).sincVal->length();
        for (int j = 0; j < bufLen; j++)
            baddata->append(0);
    }
    // Заполнение кадра
    QVector <char> badvData = baddata->toVector();
    delete baddata;
    badFrame->frameCNT = -1;
    badFrame->data = bitToByte(badvData);
    badFrame->frameErRate = int(pow(2, 16));
    badFrame->sincPos = frames.last()->sincPos + frameParam.lenFrame;
    badFrame->countValidSign = false;
    badFrame->timeFrameS.setHMS(0,0,0);
    return badFrame;
}


/*  Функция оценивания правильности счетчика кадров.
Просматривает на три кадра назад. Если между последним (-1) и предпоследним (-2),
а затем между предпоследним (-2) и предпредпоследним (-3) инкремент составил 1,
то всем трем кадрам присваивается признак валидного счетчика.
    Затем скольжением к началу осуществляется локализация окна невалидности счетчика, контролируется
правильность заполнения кадровой структуры, при необходимости - добавление/удаление сбойных кадров*/
void frameSaver::checkCount()
{
    // Входное условие
    // Проверка frames.length() должна быть >= 3
    if (frames.length() < 4)
        return;

    // Основная ветка для хорошего сигнала
    // Проверка, является ли предыдущий счетчик валидным и равен ли инкремент 1
    if (frames.at(frames.length()-2)->countValidSign &&
            abs(int(frames.at(frames.length()-1)->frameCNT -
                    frames.at(frames.length()-2)->frameCNT)) == 1)
    {
        frames.at(frames.length()-1)->countValidSign = true;
        return;
    }

    // Ветка для первого раза или после сбоя
    // Проверка величины приращения счетчика в последних трех кадрах
    if (abs(int(frames.at(frames.length()-1)->frameCNT - frames.at(frames.length()-2)->frameCNT)) != 1 ||
            abs(int(frames.at(frames.length()-2)->frameCNT - frames.at(frames.length()-3)->frameCNT)) != 1 ||
            abs(int(frames.at(frames.length()-3)->frameCNT - frames.at(frames.length()-4)->frameCNT)) != 1)
        // Если счетчик рваный - сразу выход
        return;
    else
        // Если счетчик нормальный - присвоение признака валидности счетчика и погнали на анализ
    {
        // Присвоение признака валидности счетчика трем кадрам
        frames.at(frames.length()-4)->countValidSign = true;
        frames.at(frames.length()-3)->countValidSign = true;
        frames.at(frames.length()-2)->countValidSign = true;
        frames.at(frames.length()-1)->countValidSign = true;

        // Поиск окна невалидности от конца
        int begInvalidWin = 0; // Начало окна невалидности счетчика
        int endInvalidWin = 0; // Конец окна невалидности счетчика
        int numCurFrame = frames.length() - 4; // Номер текущего кадра
        // Поиск endInvalidWin
        while (numCurFrame >= 0)
        {
            if (frames.at(numCurFrame)->countValidSign == false)
            {
                endInvalidWin = numCurFrame;
                break;
            }
            numCurFrame--;
        }
        if (!endInvalidWin)
            return;
        // Поиск begInvalidWin
        numCurFrame--;
        while (numCurFrame >= 0)
        {
            if (frames.at(numCurFrame)->countValidSign == true)
            {
                begInvalidWin = numCurFrame + 1;
                break;
            }
            numCurFrame--;
        }
        if (!begInvalidWin)
            return;

        // Проверка на количество вставленных кадров по счетчикам
        int diffNumFrames = int(endInvalidWin - begInvalidWin) + 2 - //Величина окна
                abs(int(frames.at(endInvalidWin + 1)->frameCNT - frames.at(begInvalidWin - 1)->frameCNT)); // Разность по счетчику
        // Если diffNumFrames = 0 - норма.
        if (diffNumFrames == 0)
        {
            countRecovery(begInvalidWin, endInvalidWin);
            return;
        }
        // Если diffNumFrames < 0 - нужно вставить diffNumFrames кадров.
        int indFrameMaxEr;
        qint64 diffBitPos;
        if (diffNumFrames < 0)
        {
            indFrameMaxEr = findFirstMaxErr(begInvalidWin, endInvalidWin);
            strToLog = "frameSaver: From COUNT added " + QString::number(abs(diffNumFrames))
                    + " bad frames in place " + QString::number(indFrameMaxEr);
            qDebug() << strToLog;
            emit sendStrToLog(strToLog);
            while (diffNumFrames < 0)
            {
                // Проверка на объем
                diffBitPos = frames.at(endInvalidWin + 1)->sincPos - frames.at(begInvalidWin - 1)->sincPos;
                if ((frameParam.lenFrame * abs(diffNumFrames)) >
                        (diffBitPos * (1 + float(frameParam.offsetSincFail)/100)))
                {
                    frames.at(frames.length()-3)->countValidSign = false;
                    frames.at(frames.length()-2)->countValidSign = false;
                    frames.at(frames.length()-1)->countValidSign = false;
                    return;
                }
                // Добавление
                frames.insert(indFrameMaxEr, getBadFrame());
                endInvalidWin++;
                diffNumFrames++;
            }
            countRecovery(begInvalidWin, endInvalidWin);
            return;
        }
        // Если diffNumFrames > 0 - нужно удалить diffNumFrames кадров.
        if (diffNumFrames > 0)
        {
            while (diffNumFrames > 0)
            {
                // Проверка на объем
                diffBitPos = frames.at(endInvalidWin + 1)->sincPos - frames.at(begInvalidWin - 1)->sincPos;
                if ((frameParam.lenFrame * abs(diffNumFrames)) <
                        (diffBitPos * (1 + float(frameParam.offsetSincFail)/100)))
                {
                    frames.at(frames.length()-3)->countValidSign = false;
                    frames.at(frames.length()-2)->countValidSign = false;
                    frames.at(frames.length()-1)->countValidSign = false;
                    return;
                }
                // Удаление
                indFrameMaxEr = findFirstMaxErr(begInvalidWin, endInvalidWin);
                frames.removeAt(indFrameMaxEr);
                endInvalidWin--;
                strToLog = "frameSaver: From COUNT deleted frame " + QString::number(indFrameMaxEr) +
                        ".\tNum frames:" + QString::number(frames.length());
                qDebug() << strToLog;
                emit sendStrToLog(strToLog);
                diffNumFrames--;
            }
            countRecovery(begInvalidWin, endInvalidWin);
            return;
        }
    }
}


/*Поиск индекса первого элемента с максимальным количеством ошибок в заданном диапазоне*/
int frameSaver::findFirstMaxErr(int beg, int end)
{
    int indFrameMaxEr = beg;
    int maxErr = 0;
    for (int i = beg; i <= end; i++)
        if (frames.at(i)->frameErRate > maxErr)
        {
            maxErr = frames.at(i)->frameErRate;
            indFrameMaxEr = i;
        }
    return indFrameMaxEr;
}


void frameSaver::countRecovery(int beg, int end)
{
    bool direction = true; // По умолчанию счетчик считает вперед
    if (((frames.at(beg - 1)->frameCNT) - (frames.at(beg - 2)->frameCNT)) < 0)
        direction = false;
    for (int i = beg; i <= end; i++)
        if (direction)
            if ((frames.at(i - 1)->frameCNT + 1) > maxCountVal)
            {
                frames.at(i)->frameCNT = 0;
                frames.at(i)->countValidSign = true;
                strToLog = "frameSaver: Recovery count: " + QString::number(0);
                qDebug() << strToLog;
                emit sendStrToLog(strToLog);
            }
            else
            {
                frames.at(i)->frameCNT = frames.at(i - 1)->frameCNT + 1;
                frames.at(i)->countValidSign = true;
                strToLog = "frameSaver: Recovery count: " + QString::number(frames.at(i)->frameCNT);
                qDebug() << strToLog;
                emit sendStrToLog(strToLog);
            }
        else
            if ((frames.at(i - 1)->frameCNT) == 0)
            {
                frames.at(i)->frameCNT = maxCountVal;
                frames.at(i)->countValidSign = true;
                strToLog = "frameSaver: Recovery count: " + QString::number(maxCountVal);
                qDebug() << strToLog;
                emit sendStrToLog(strToLog);
            }
            else
            {
                frames.at(i)->frameCNT = frames.at(i - 1)->frameCNT - 1;
                frames.at(i)->countValidSign = true;
                strToLog = "frameSaver: Recovery count: " + QString::number(frames.at(i)->frameCNT);
                qDebug() << strToLog;
                emit sendStrToLog(strToLog);
            }
}


void frameSaver::countRestor()
{
    QList <qint64> countList;
    for (int j = 0; j < frames.length(); j++)
    {
        countList.append(frames.at(j)->frameCNT);
        strToLog = "frameSaver: Frame:\t" + QString::number(j) +
                ".\tCount:\t" + QString::number(countList.at(j));
        emit sendStrToLog(strToLog);
    }
}


frameSaver::~frameSaver()
{
    for (int i = 0; i < frames.length(); i++)
    {
        frames.at(i)->data.clear();
        frames.at(i)->data.squeeze();
    }
    frames.clear();
    //frames.squeeze();
    qDebug() << "frameSaver: Destructor!";
}
