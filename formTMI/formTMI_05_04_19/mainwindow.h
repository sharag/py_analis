#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "common.h"
#include "dmxthread.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButtonOpenInDIR_clicked();
    void on_pushButtonStart_clicked();
    void progress_update(int value, QString str);
    void numFrameUpdate(QString);
    void DMXthreadStopped(bool);
    void initError(QString);

private:
    Ui::MainWindow *ui;
    void set_out_file_name(QStringList str);
    bool getSinc(QVector <sincParamSt>* sincVect, int lenFrame);
    QStringList inFiles;
    bool processingSign = false;
    DMXThread * commonDmx;

signals:
    void sendNeedStop(bool);
};

#endif // MAINWINDOW_H
