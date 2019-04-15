#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <dmxthread.h>
#include <QMimeData>
#include "common.h"


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
    bool getSinc(QList <sincParamSt>* sincVect, int lenFrame);
    QStringList inFiles;
    bool processingSign = false;
    DMXThread * commonDmx;
    void addInFileNames(QStringList fileList);

protected:
    void dragEnterEvent(QDragEnterEvent* event);
    void dropEvent(QDropEvent* event);

signals:
    void sendNeedStop(bool);
};

#endif // MAINWINDOW_H
