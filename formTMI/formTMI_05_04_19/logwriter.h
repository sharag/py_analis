#ifndef LOGWRITER_H
#define LOGWRITER_H

#include <QObject>
#include <QFile>

class logWriter : public QObject
{
    Q_OBJECT

public:
    logWriter(QString outFile);
    ~logWriter();

public slots:
    void sendToLog(QString str);

private slots:
    void writeToFile();

private:
    QFile logFile;
    QStringList logList;
    QString logFName;

signals:
    void sendError(QString);
    void needWriteToLog(bool);
};

#endif // LOGWRITER_H
