#include "mainwindow.h"
#include <QApplication>

using namespace std;

int main(int argc, char *argv[])
{
    QApplication formTMI(argc, argv);
    MainWindow winFormTMI;
    winFormTMI.show();

    return formTMI.exec();
}
