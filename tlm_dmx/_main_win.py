#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import sys
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QMainWindow, QAction, qApp
# QToolTip, QPushButton,
from PyQt5.QtGui import QIcon  # , QFont
# from PyQt5.QtCore import QCoreApplication
from _centr_widg import MainWidg


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Параметры основного окна # self.resize(250, 150) # QToolTip.setFont(QFont('SansSerif', 10))
        self.setGeometry(0, 0, 800, 600)
        self.center()
        self.setWindowTitle('Экспресс-анализ ТМИ')
        self.setWindowIcon(QIcon('./icons/icon.png'))
        # self.setToolTip('Главное окно программного комплекса <b>Экспресс-анализ ТМИ<b>')  # Текст подсказки.
        # Действие на выход
        self.exitAction = self.exit_action_init()
        self.open_db_action = self.open_db_action_init()
        # Установка центрального виджета
        self.c_widget = MainWidg(self)
        self.setCentralWidget(self.c_widget)
        # Статус бар
        self.statusBar().showMessage('Готов')
        # Меню программы
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&Файл')
        file_menu.addAction(self.open_db_action)
        file_menu.addAction(self.exitAction)
        # Туулбар
        self.toolbar = self.addToolBar('Выход')
        self.toolbar.addAction(self.open_db_action)
        self.toolbar.addAction(self.exitAction)
        # Показать все
        self.show()

    def show_satus(self, text):
        self.statusBar().showMessage(text)

    def open_db_action_init(self):
        self.open_db_action = QAction(QIcon('./icons/file open.png'), 'Выбор файла БД', self)
        self.open_db_action.setShortcut('Ctrl+O')
        self.open_db_action.setStatusTip('Выбор файла БД')
        # self.open_db_action.triggered.connect(self.dialog_select_db)
        self.open_db_action.triggered.connect(self.dialog_select_db)
        return self.open_db_action

    def dialog_select_db(self):
        self.c_widget.select_db_btn_click()

    def exit_action_init(self):
        self.exitAction = QAction(QIcon('./icons/exit.png'), 'Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Выход из приложения')
        self.exitAction.triggered.connect(self.exit_msg)
        return self.exitAction

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Экспресс-анализ ТМИ', "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def exit_msg(self):
        reply = QMessageBox.question(self, 'Экспресс-анализ ТМИ', "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            qApp.quit()  # QCoreApplication.instance().quit()
            
    def eof_msg(self, text):
        QMessageBox.information(self, 'Внимание!', 'Декоммутация завершена!', buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)

    def err_msg(self, text):
        QMessageBox.warning(self, 'Внимание!', ('Ошибка: ' + text), buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)
