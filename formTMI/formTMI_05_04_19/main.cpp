#include "mainwindow.h"
#include <QApplication>

using namespace std;

int main(int argc, char *argv[])
{
    QStringList paths = QCoreApplication::libraryPaths();
    paths.append(".");
    //paths.append("imageformats");
    paths.append("platforms");
    //paths.append("sqldrivers");
    QCoreApplication::setLibraryPaths(paths);


    QApplication formTMI(argc, argv);
    MainWindow winFormTMI;
    winFormTMI.show();

    return formTMI.exec();
}
