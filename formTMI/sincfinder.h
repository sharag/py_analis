#ifndef SINCFINDER_H
#define SINCFINDER_H

#include "common.h"
#include "filereader.h"
#include <QVector>


class sincFinder
{
public:
    sincFinder(QVector <sincParamSt> sincVect_,
               frameParamSt frameParam_,
               fileReader* inFReader_);
    qint64 findNextFrame(qint64 startBit, QVector <sincFindRezSt*>* rezultsSinc);

private:
    QVector <sincParamSt> sincVect;
    fileReader* inFReader;
    frameParamSt frameParam;
    qint64 syncPos;
    qint64 findNextSinc(int itSinc,
                        qint64 startBit,
                        QVector <sincFindRezSt*>* rezultsSinc);
    //QVector <sincParamRaw*> sincVectRaw;
    bool checkFirst(int itSinc);
    bool checkLast(int itSinc);
    bool checkHam(QVector<char>* bufForVerify,
                  sincFindRezSt* rezultsSinc,
                  int itSinc,
                  int hamDist);
};

#endif // SINCFINDER_H
