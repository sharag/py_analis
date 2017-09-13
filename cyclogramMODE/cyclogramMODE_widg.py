import os
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QAbstractItemView
from PyQt5.QtWidgets import QGroupBox, QLabel, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QSpinBox, QFileDialog, QMessageBox, QHeaderView


import pyqtgraph as pg
import numpy as np
from cyclogramMODE.cyclogramMODE_thread import CyclogrModeThread


class CyclogrModeMainWidg(QWidget):
    def __init__(self, path, num_order):
        super().__init__()
        self.init_var()
        self.init_ui()

    def init_var(self):
        self.fname = None
        self.num_order = None
        self.thread = None

    def init_ui(self):

        # Описание модуля
        self.lbl_descr = self.lbl_descr_init()

        # Настройка параметров поиска
        self.gbox_path = QGroupBox('Выберите файл с каналом режимов...')
        self.gbox_path.setMaximumWidth(600)
        self.btn_path = self.btn_path_init()
        self.lbl_path = QLabel('')
        self.lbl_path.setWordWrap(True)
        self.lbl_path.setMaximumWidth(600)
        self.lbl_numord = QLabel('Количество разрядов телеметрического канала')
        self.spin_numord = self.spin_numord_init()

        # График
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.grafik = pg.PlotWidget(name='Plot1')
        self.grafik.setLabel('left', '<font size="5">Амплитуда</font>')
        # self.grafik.setLabel('bottom', '<font size="5">Время, (c)</font>', units='с')
        self.grafik.setLabel('bottom', '<font size="5">Время, (c)</font>')
        # self.grafik.setXRange(0, 2)
        # self.grafik.setYRange(0, 1e-10)

        # Таблица с результатами работы (с циклограммой)
        self.table_cycl = QTableWidget()
        self.table_cycl.setRowCount(0)
        self.table_cycl.setColumnCount(3)
        self.table_cycl.setHorizontalHeaderLabels(["№", "Время", "Характеристика"])
        self.table_cycl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_cycl.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования таблицы
        self.table_cycl.setMaximumWidth(600)
        # self.table_cycl.setWordWrap(True)
        # self.table_cycl.setColumnWidth(номер столбца, ширина)
        # table.setVerticalHeaderLabels(["", ""])

        # Управление макетом
        self.cur_layout = self.layout_init()
        self.setLayout(self.cur_layout)

    def lbl_descr_init(self):
        descr = '<div align="center">Программа расчета циклограммы полета БР по каналу режимов.</div>'
        self.lbl_descr = QLabel(descr)
        self.lbl_descr.setMaximumWidth(500)
        self.lbl_descr.setWordWrap(True)
        self.lbl_descr.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        return self.lbl_descr

    def btn_path_init(self):
        self.btn_path = QPushButton('Выбрать...')
        self.btn_path.resize(self.btn_path.sizeHint())
        self.btn_path.clicked.connect(self.show_dlg_path)
        self.btn_path.setStatusTip('Выбор файла ...')
        return self.btn_path

    def spin_numord_init(self):
        self.spin_numord = QSpinBox(self)
        self.spin_numord.setMinimumWidth(40)
        self.spin_numord.setMaximumWidth(60)
        self.spin_numord.setValue(16)
        self.spin_numord.setMaximum(64)
        self.spin_numord.setMinimum(8)
        self.spin_numord.setSingleStep(8)
        self.spin_numord.valueChanged.connect(self.spin_numord_chng)
        self.spin_numord.editingFinished.connect(self.get_numord)
        self.spin_numord.setStatusTip('Введите количество разрядов телеметрических каналов')
        return self.spin_numord

    def spin_numord_chng(self):
        if self.spin_numord.value() < 8:
            self.spin_numord.setValue(8)
        elif self.spin_numord.value() > 64:
            self.spin_numord.setValue(64)

    def show_dlg_path(self):
        dir_path = '..'
        dlg_files = QFileDialog()
        dlg_files.setFileMode(QFileDialog.AnyFile)
        dlg_files.setLabelText(QFileDialog.LookIn, 'Открыть файл канала режимов ...')
        dlg_files.setAcceptMode(QFileDialog.AcceptOpen)
        dlg_files.setDirectory(dir_path)
        if dlg_files.exec_():
            self.table_cycl.clear()
            self.table_cycl.setRowCount(0)
            self.table_cycl.setColumnCount(3)
            self.table_cycl.setHorizontalHeaderLabels(["№", "Время", "Характеристика"])
            self.fname = dlg_files.selectedFiles()[0]
            self.lbl_path.setText(self.fname)
            if self.thread is not None:
                self.thread.disconnect()
                self.thread = None
            self.num_order = self.get_numord()
            self.setStatusTip('Идет обработка...')
            self.thread = CyclogrModeThread(self.fname, self.num_order, self.grafik)
            self.thread.s_error[str].connect(self.showDlgErr)
            self.thread.finished.connect(self.finished_cyclogr_mode_thread)
            self.thread.s_mode.connect(self.update_table)
            self.thread.start()

    def update_table(self, i):
        if i[0] == 0:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1]/100)))
            descr = 'Участок старта и неуправляемого полета'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 1:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Управляемый полет первой ступени и разделение ступеней'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 2:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Управляемый полет второй ступени и разделение ступеней, отделение головного обтекателя'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 3:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Управляемый полет третьей ступени'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 4:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Участок дожигания топлива'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 5:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Совместный полет третьей ступени и АБР, отход АБР'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 6:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Разворот АБР'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 7:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Астрокоррекция параметров СУ'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 8:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Разворот АБР в точку прицеливания'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 9:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Отработка командного вектора, в заданном направлении'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 10:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Разворот и успокоение АБР для сброса БГ'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 11:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Стабилизация и сброс БГ, отход АБР от БГ с разворотом'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        elif i[0] == 12 or i[0] == 13 or i[0] == 14:
            self.table_cycl.insertRow(self.table_cycl.rowCount())
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 0, QTableWidgetItem(str(i[0])))
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 1, QTableWidgetItem(str(i[1] / 100)))
            descr = 'Движение в направлении, заданном предыдущим разворотом (в течении режима 11)'
            self.table_cycl.setItem(self.table_cycl.rowCount() - 1, 2, QTableWidgetItem(descr))
        return

    def showDlgErr(self, err):
        dlg_err = QMessageBox()
        dlg_err.setIcon(QMessageBox.Warning)
        dlg_err.setWindowTitle('Ошибка')
        dlg_err.setText(err)
        dlg_err.setStandardButtons(QMessageBox.Ok)
        dlg_err.exec_()

    def finished_cyclogr_mode_thread(self):
        if self.thread is not None:
            self.thread.disconnect()
            self.thread = None
        self.setStatusTip('')

    def get_numord(self):
        condition = self.spin_numord.value() != 8 and self.spin_numord.value() != 16 and self.spin_numord.value() != 32
        condition = condition and self.spin_numord.value() != 64
        if condition:
            if self.spin_numord.value() <= 8:
                self.spin_numord.setValue(8)
            elif self.spin_numord.value() <= 16:
                if self.spin_numord.value() < 12:
                    self.spin_numord.setValue(8)
                else:
                    self.spin_numord.setValue(12)
            elif self.spin_numord.value() < 32:
                if self.spin_numord.value() < 24:
                    self.spin_numord.setValue(16)
                else:
                    self.spin_numord.setValue(32)
            else:
                if self.spin_numord.value() < 48:
                    self.spin_numord.setValue(32)
                else:
                    self.spin_numord.setValue(64)
        return self.spin_numord.value()

    def layout_init(self):
        # Предназначение
        descr_layout = QHBoxLayout()
        descr_layout.addWidget(self.lbl_descr)
        # Выбор файла
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.btn_path)
        path_layout.addStretch(1)
        path_v_layout = QVBoxLayout()
        path_v_layout.addLayout(path_layout)
        path_v_layout.addWidget(self.lbl_path)
        self.gbox_path.setLayout(path_v_layout)
        # Параметры
        param_layout = QVBoxLayout()
        param_layout.addWidget(self.lbl_numord)
        param_layout.addWidget(self.spin_numord)
        # Левый layout
        vbox_left = QVBoxLayout()
        vbox_left.addLayout(descr_layout)
        self.gbox_path.setMaximumWidth(500)
        vbox_left.addWidget(self.gbox_path)
        vbox_left.addLayout(param_layout)
        vbox_left.addWidget(self.table_cycl)
        #vbox_left.addStretch(1)
        # График
        hbox_stretch = QHBoxLayout()
        hbox_stretch.addStretch(1)
        hbox_stretch.addStretch(1)
        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.grafik)
        vbox_right.addLayout(hbox_stretch)
        # Итоговый layout
        hbox_common = QHBoxLayout()
        hbox_common.addLayout(vbox_left)
        hbox_common.addLayout(vbox_right)
        return hbox_common
