from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon
from searchBitChange.searchBitChange_widg import SBitChange_MainWidg

'''Основное окошко программы '''


class SbitChangeMainWin(QMainWindow):

    def __init__(self, path, num_order, num_bit, min_num_chng, max_num_chng):
        super().__init__()
        self.init_ui(path, num_order, num_bit, min_num_chng, max_num_chng)
        
    def init_ui(self, path, numOrder, numberBit, minNumChange, maxNumChange):
        self.setWindowTitle('Поиск разрядов с указанным количеством изменений')
        self.setWindowIcon(QIcon('./icons/icon.png'))
        # Действие на выход
        self.exitAction = self.exit_action_init()
        # Статус бар
        self.statusBar().showMessage('Готов')
        # Установка центрального виджета
        self.c_widget = SBitChange_MainWidg(path, numOrder, numberBit, minNumChange, maxNumChange)
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
        reply = QMessageBox.question(self, 'Поиск разрядов с указанным количеством изменений', "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            qApp.quit()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Программа поиска разрядов с указанным количеством изменений', "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()