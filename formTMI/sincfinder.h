#ifndef SINCFINDER_H
#define SINCFINDER_H

#include "common.h"
#include "filereader.h"
#include <QVector>


class sincFinder
{
public:
    sincFinder(QList <sincParamSt>* sincVect_,
               frameParamSt* frameParam_,
               fileReader* inFReader_);
    qint64 findNextFrame(qint64 startBit,
                         QList <sincFindRezSt*>* rezultsSinc);

private:
    QList <sincParamSt>* sincVect;
    fileReader* inFReader;
    frameParamSt* frameParam;
    qint64 syncPos;
    qint64 findNextSinc(int itSinc,
                        qint64 startBit,
                        QList <sincFindRezSt*>* rezultsSinc);
    bool checkFirst(int itSinc);
    bool checkLast(int itSinc);
    bool checkHam(QVector<char>* bufForVerify,
                  sincFindRezSt* rezultsSinc,
                  int itSinc,
                  int hamDist);
    QVector<char>* bufForVerify; // Текущий буффер для проверки
};

#endif // SINCFINDER_H
