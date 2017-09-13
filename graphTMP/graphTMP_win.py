from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon
from graphTMP.graphTMP_widg import GraphTMPMainWidg


class GraphTMPMainWin(QMainWindow):
    """Основное окошко программы"""
    def __init__(self, path, type_data, frequency):
        super().__init__()
        self.init_ui(path, type_data, frequency)

    def init_ui(self, path, type_data, frequency):
        self.setWindowTitle('Графический анализ ТМП')
        self.setWindowIcon(QIcon('../icons/icon.png'))
        # Действие на выход
        self.exitAction = self.exit_action_init()
        # Статус бар
        self.statusBar().showMessage('Готов')
        # Установка центрального виджета
        self.c_widget = GraphTMPMainWidg(path, type_data, frequency)
        self.setCentralWidget(self.c_widget)
        # Показать все
        self.show()

    def exit_action_init(self):
        self.exitAction_ = QAction(QIcon('./icons/exit.png'), 'Выход', self)
        self.exitAction_.setShortcut('Ctrl+Q')
        self.exitAction_.setStatusTip('Выход из приложения')
        self.exitAction_.triggered.connect(self.exit_msg)
        return self.exitAction_

    def exit_msg(self):
        reply = QMessageBox.question(self, 'Графический анализ ТМП',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            qApp.quit()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Графический анализ ТМП',
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
