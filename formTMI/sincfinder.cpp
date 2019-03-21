#include "sincfinder.h"
#include "bytetobit.h"
#include "QDebug"
#include "common.h"


int calc_hamming(QVector<char> *buff, QVector<char> *sinc)
{
    int dist = 0;
    for (int i = 0; i < buff->length(); i++)
        if (buff->at(i) != sinc->at(i))
            dist++;
    return dist;
}


sincFinder::sincFinder(QVector <sincParamSt> sincVect_,
                       frameParamSt frameParam_,
                       fileReader* inFReader_)
{
    sincVect = sincVect_;
    frameParam = frameParam_;
    syncPos = 0;
    inFReader = inFReader_;
    qDebug() << "sincFinder: Frame sinc initializing.";
}


/*Возвращает позицию начала очередного кадра после startBit*/
qint64 sincFinder::findNextFrame(qint64 startBit, QVector <sincFindRezSt*>* rezultsSinc)
{
    int startNumSinc = 0;
    syncPos = findNextSinc(startNumSinc,
                           startBit,
                           rezultsSinc);
    return syncPos;
}


/*Возвращает позицию очередной синхрокомбинации или -1
-1 - это отсутствие СК на месте
>=0 - позиция СК в кадре*/
qint64 sincFinder::findNextSinc(int itSinc,
                                qint64 startBit, // Номер искомой синхрокомбинации из вектора sincVect
                                QVector <sincFindRezSt*>* rezultsSinc)
{
    int sincLen = sincVect.at(itSinc).sincVal->length(); // Длина синхрокомбинации
    QVector<char> bufForVerify(sincLen); // Текущий буффер для проверки
    int hamDist = sincVect.at(itSinc).hammingDistVal; // Расстояние Хэмминга
    int bitOffset = int(float(frameParam.offsetSincFail)/100*frameParam.lenFrame); // Смещение относительно startBit
    qint64 curBitPos = 0; // Текущая позиция
    int sincOffset = 0; // Смещение позиций синхронизации друг относительно друга
    qint64 maxChildPos = startBit + bitOffset; // Позиция дочерней СК с максимальным смещением

    curBitPos = startBit;
    bufForVerify = inFReader->getBits(curBitPos, sincLen);
    if (bufForVerify.length() != sincLen)
        return -1;

    // Проверка на позиции startBit
    if (checkHam(&bufForVerify,
                 rezultsSinc->at(itSinc),
                 itSinc,
                 hamDist))
    {
        //Если СК последняя
        if (checkLast(itSinc))
        {
            rezultsSinc->at(itSinc)->sincPos = curBitPos;
            return curBitPos; // Возврат позиции
        }
        // Если СК не последняя - вызов рекурсии
        else
        {
            sincOffset = sincVect.at(itSinc + 1).sincPos - sincVect.at(itSinc).sincPos;
            // Вызов рекурсии
            if (findNextSinc(itSinc + 1, curBitPos + sincOffset, rezultsSinc) > 0)
            {// Если дочерняя СК на месте - возврат позиции
                rezultsSinc->at(itSinc)->sincPos = curBitPos;
                return curBitPos; // Возврат позиции
            }
        }
    }

    // Если на позиции startBit СК не обнаружена
    curBitPos = startBit - bitOffset; // Отступ на (startBit-5%(lenFrame))
    if (curBitPos < 0) // Проверка, если мы в самом начале файла, то нельза запрашивать отрицательные значения
        curBitPos = 0;
    bufForVerify = inFReader->getBits(curBitPos, sincLen);
    if (bufForVerify.length() != sincLen)
        return -1;
    // Скольжение Цикл while
    while (true)
    {
        if (checkHam(&bufForVerify,
                     rezultsSinc->at(itSinc),
                     itSinc,
                     hamDist))
        {
            //Если СК последняя
            if (checkLast(itSinc))
            {
                rezultsSinc->at(itSinc)->sincPos = curBitPos;
                return curBitPos; // Возврат позиции
            }
            // Если СК не последняя - вызов рекурсии
            else
            {
                sincOffset = sincVect.at(itSinc + 1).sincPos - sincVect.at(itSinc).sincPos;
                // Вызов рекурсии
                if (findNextSinc(itSinc + 1, curBitPos + sincOffset, rezultsSinc) > 0)
                {
                    rezultsSinc->at(itSinc)->sincPos = curBitPos;
                    return curBitPos; // Если дочерняя СК на месте - возврат позиции
                }
            }
        }
        curBitPos++; // Изменение текущей позиции
        bufForVerify = inFReader->getBits(curBitPos, sincLen);
        if (bufForVerify.length() != sincLen)
            return -1;
        if (checkFirst(itSinc))
            continue;
        else
            if (curBitPos > maxChildPos)
                return -1;
    }
}


bool sincFinder::checkFirst(int itSinc)
{
    if (itSinc == 0)
        return true;
    else
        return false;
}


bool sincFinder::checkLast(int itSinc)
{
    if (itSinc == (sincVect.length() - 1))
        return true;
    else
        return false;
}


bool sincFinder::checkHam(QVector<char>* bufForVerify,
                          sincFindRezSt* rezultsSinc,
                          int itSinc,
                          int hamDist)
{
    int factHam = calc_hamming(bufForVerify, sincVect.at(itSinc).sincVal);
    if (factHam <= hamDist)
    {
        rezultsSinc->inverseSign = false;
        rezultsSinc->numErr = factHam;
        return true;
    }
    factHam = calc_hamming(bufForVerify, sincVect.at(itSinc).sincValRev);
    if (factHam <= hamDist)
    {
        rezultsSinc->inverseSign = true;
        rezultsSinc->numErr = factHam;
        return true;
    }
    return false;
}
