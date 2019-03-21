#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "QFileDialog"
#include "QMessageBox"
#include "QStringList"
#include "QString"
#include "QFile"
#include "QDir"
#include "QDebug"
#include "dmxthread.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->pushButtonStart->setDisabled(true);
    ui->statusBar->showMessage("Нажмите кнопку Старт!");
}


void MainWindow::on_pushButtonOpenInDIR_clicked()
{
    QString filename;//переменная содержащая путь к файлу
    //создание нового окна для выбора каталога
    QStringList str = QFileDialog::getOpenFileNames(
                this,
                "Выберите файлы ГТС",
                "C:\\",
                "Файлы ГТС (*.bit *.bi1)");
    if (!str.isEmpty())
    {
        inFiles = str;
        set_out_file_name(str);
        for (int i = 0; i < str.length(); i++)
            str[i] = QDir().toNativeSeparators(str.at(i));
        ui->textEditInDIR->setText(str.join(QChar('\n')));
        ui->pushButtonStart->setEnabled(true);
    }
    return;
}


// Проверка корректности имени файла и заполнение поля выходного каталога
void MainWindow::set_out_file_name(QStringList str)
{
    QString outStr = str.at(0);
    QStringList temp = outStr.split('/');
    temp.removeAt(temp.length() - 1);
    outStr = temp.join('/');
    outStr.append('/');
    outStr.append("out.bi1");
    // в поле выводится каталог для создания под разуплотненные файлы
    ui->textEditRezDir->setText(QDir().toNativeSeparators(outStr));
    return;
}


void MainWindow::on_pushButtonStart_clicked()
{
    // Если процесс обработки идет, значит нажата кнопка "Стоп"
    if (processingSign)
    {
        emit sendNeedStop(true);
        return;
    }

    //Проверки
    // Файлы
    if (inFiles.isEmpty())//Проверка , выбраны ли файлы
    {
        QMessageBox::warning(this,
                             "ВНИМАНИЕ",
                             "Выберите файлы ГТС!");
        return;
    }
    for (int i = 0; i < inFiles.length(); i++) //Проверка существования файлов
        if (!QFile(inFiles.at(i)).exists())
        {
            QMessageBox::warning(this,
                                 "ВНИМАНИЕ",
                                 "Исходного файла не существует!");
            return;
        }
    // Параметры:
    frameParamSt frameParam;
    QString outFname = ui->textEditRezDir->document()->toPlainText();
    frameParam.lenWord = ui->spinBoxLenChan->value();//Длина слова
    frameParam.lenFrame = ui->spinBoxLenFrame->value();//Длина кадра
    frameParam.offsetSincFail = ui->spinBoxOffsetSincFail->value(); // Смещение срыва синхронизации
    frameParam.freqFrame = ui->spinBoxFreqFrame->value(); // Частота следования кадров
    if (frameParam.lenFrame % frameParam.lenWord)//Если существует остаток от деления на длину слова
    {
        QMessageBox::warning(this,
                             "ВНИМАНИЕ",
                             "Заданы неверные параметры кадрообразования!");
        return;
    }
    // Синхрокомбинация
    QVector <sincParamSt> sincVect;
    if (!getSinc(&sincVect,
                 frameParam.lenFrame))
        return;
    // Счетчик
    countParamSt countParam;
    countParam.countLen = ui->spinBoxCountLen->value();
    countParam.countPos = ui->spinBoxCountPos->value() - 1;
    countParam.joinFramesSign = ui->checkBoxJoinFrames->isChecked();
    //Создание объекта класса DMXThread
    commonDmx = new DMXThread(inFiles,
                              outFname,
                              frameParam,
                              sincVect,
                              countParam);
    // Коннекты
    connect(commonDmx,
            SIGNAL(sendProgress(int,
                                QString)),
            this,
            SLOT(progress_update(int,
                                 QString)));
    connect(commonDmx,
            SIGNAL(sendNumFrames(QString)),
            this,
            SLOT(numFrameUpdate(QString)));
    connect(commonDmx,
            SIGNAL(sendStopped(bool)),
            this,
            SLOT(DMXthreadStopped(bool)));
    connect(this,
            SIGNAL(sendNeedStop(bool)),
            commonDmx,
            SLOT(needStop(bool)));
    connect(commonDmx,
            SIGNAL(sendError(QString)),
            this,
            SLOT(initError(QString)));
    // Настройка морды к обработке
    processingSign = true; // Признак существования процесса обработки
    ui->pushButtonStart->setText("Стоп");
    ui->pushButtonOpenInDIR->setDisabled(true);
    ui->statusBar->showMessage("Обработка: ");
    // Стааарт!!
    commonDmx->start();
}


bool MainWindow::getSinc(QVector <sincParamSt>* sincVect,
                         int lenFrame)
{
    //№1
    sincParamSt sinc;
    if (ui->lineEditSinc1->text().length() < 8 ||
            (ui->spinBoxSync1Pos->value() + ui->lineEditSinc1->text().length()) >= lenFrame ||
            ui->spinBoxSync1Pos->value() < 1)
    {
        QMessageBox::warning(this,
                             "ВНИМАНИЕ",
                             "Заданы неверные параметры синхрокомбинации №1!");
        return false;
    }
    sinc.sincStr = ui->lineEditSinc1->text();
    sinc.sincPos = ui->spinBoxSync1Pos->value() - 1;
    sinc.hammingDistVal = ui->spinBoxHamDist1->value();
    sincVect->append(sinc);
    //№2
    if (ui->lineEditSinc2->text().length())
    {
        if (ui->lineEditSinc2->text().length() < 8 ||
                (ui->spinBoxSync2Pos->value() + ui->lineEditSinc2->text().length()) >= lenFrame ||
                ui->spinBoxSync2Pos->value() < 1)
        {
            QMessageBox::warning(this,
                                 "ВНИМАНИЕ",
                                 "Заданы неверные параметры синхрокомбинации №2!");
            return false;
        }
        sinc.sincStr = ui->lineEditSinc2->text();
        sinc.sincPos = ui->spinBoxSync2Pos->value() - 1;
        sinc.hammingDistVal = ui->spinBoxHamDist2->value();
        sincVect->append(sinc);
    }
    //№3
    if (ui->lineEditSinc3->text().length())
    {
        if (ui->lineEditSinc3->text().length() < 8 ||
                (ui->spinBoxSync3Pos->value() + ui->lineEditSinc3->text().length()) >= lenFrame ||
                ui->spinBoxSync3Pos->value() < 1)
        {
            QMessageBox::warning(this,
                                 "ВНИМАНИЕ",
                                 "Заданы неверные параметры синхрокомбинации №3!");
            return false;
        }
        sinc.sincStr = ui->lineEditSinc3->text();
        sinc.sincPos = ui->spinBoxSync3Pos->value() - 1;
        sinc.hammingDistVal = ui->spinBoxHamDist3->value();
        sincVect->append(sinc);
    }

    // Сортировка синхронизаций по позиции
    if (sincVect->length() > 1)
        for (int j = 1; j < sincVect->length(); j++) //Упорядочивание элементов в массиве по возрастанию их значений
            for (int i = 0; i < sincVect->length() - j; i++)
                if (sincVect->at(i).sincPos > sincVect->at(i + 1).sincPos) //Если текущий элемент больше следующего
                {
                    sincParamSt temp = sincVect->at(i); //Сохранить значение текущего элемента
                    sincVect->replace(i, sincVect->at(i + 1)); //Заменить текущий элемент следующим
                    sincVect->replace(i + 1, temp); //Заменить следующий элемент на сохранённый в temp
                }
    return true;
}


void MainWindow::progress_update(int value,
                                 QString str)
{
    ui->progressBar->setValue(value);
    ui->statusBar->showMessage(str);
}


void MainWindow::numFrameUpdate(QString str)
{
    if (processingSign)
        ui->statusBar->showMessage(str);
}


void MainWindow::initError(QString str)
{
    QMessageBox::warning(this,
                         "ВНИМАНИЕ",
                         str);
    return;
}


void MainWindow::DMXthreadStopped(bool)
{
    //commonDmx->~DMXThread(); // Уничтожение DMXThread
    delete commonDmx; // Уничтожение DMXThread
    ui->pushButtonStart->setText("Старт");
    ui->pushButtonOpenInDIR->setEnabled(true);
    ui->progressBar->setValue(0);
    ui->statusBar->showMessage("Нажмите кнопку Старт!");
    processingSign = false; // Признак существования процесса обработки
}


MainWindow::~MainWindow()
{
    delete ui;
}

