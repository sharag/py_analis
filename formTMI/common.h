#ifndef COMMON_H
#define COMMON_H

#include <QString>
#include <QVector>
#include <QTime>


struct sincParamSt
{
    QString sincStr;
    qint64 sincPos;
    QVector <char>* sincVal;
    QVector <char>* sincValRev;
    int hammingDistVal;
};


struct countParamSt
{
    bool joinFramesSign;
    int countPos;
    int countLen;
};


struct sincFindRezSt
{
    qint64 sincPos;
    bool inverseSign;
    int numErr;
};


struct frameSt
{
    qint64 frameCNT;
    bool countValidSign;
    int frameErRate;
    QVector <char> data;
    qint64 sincPos;
    QTime timeFrameS;
};


struct frameParamSt
{
    int lenWord;
    int lenFrame;
    double offsetSincFail;
    int freqFrame;
};

#endif // COMMON_H
