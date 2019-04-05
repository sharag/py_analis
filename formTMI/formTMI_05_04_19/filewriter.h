#ifndef FILEWRITER_H
#define FILEWRITER_H

#include "QString"
#include "QFileDialog"
#include "QVector"
#include "QFile"
#include "QObject"

class fileWriter : public QObject
{
    Q_OBJECT

public:
    fileWriter(QString outF_name);
    ~fileWriter();
    void addData(QVector<char> data);
    void addData(QString CurStr);

private:
    int volBuff;
    QFile outFile;
    QVector<char>* curBuff;
    QString strToLog;
    void writeToFile();

signals:
    void sendStrToLog(QString);
    void sendError(QString);
};


namespace Ui {
class MainWindow;
}


#endif // FILEREADER_H
