from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon
from searchMODE.searchMODE_widg import SMODE_MainWidg

'''Основное окошко программы '''
class SMODE_mainwin(QMainWindow):

    def __init__(self, path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes):
        super().__init__()
        self.init_ui(path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes)
        
    def init_ui(self, path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes):
        self.setWindowTitle('Поиск канала режимов')
        self.setWindowIcon(QIcon('./icons/icon.png'))
        # Действие на выход
        self.exitAction = self.exit_action_init()
        # Статус бар
        self.statusBar().showMessage('Готов')
        # Установка центрального виджета
        self.c_widget = SMODE_MainWidg(path, timeInterval, numOrder, sampleFreq, minNumModes, maxNumModes)
        self.setCentralWidget(self.c_widget)
        # Показать все
        self.show()
        
    def exit_action_init(self):
        self.exitAction = QAction(QIcon('./icons/exit.png'), 'Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Выход из приложения')
        self.exitAction.triggered.connect(self.exit_msg)
        return self.exitAction
    
    def exit_msg(self):
        reply = QMessageBox.question(self, 'Поиск канала режимов', "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            qApp.quit()  # QCoreApplication.instance().quit()
        qApp.quit()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Программа поиска канала режимов', "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()