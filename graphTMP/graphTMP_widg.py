import os
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QDoubleSpinBox, QLabel
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QFileDialog, QMessageBox
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from graphTMP.graphTMP_thread import GraphTMPThread
# import numpy as np
# from PyQt5.QtWidgets import QSizePolicy, QTableWidget, QTableWidgetItem
# from PyQt5.QtWidgets import QSpinBox, QHeaderView, QAbstractItemView


class GraphTMPMainWidg(QWidget):
    def __init__(self, path, type_data, freq):
        super().__init__()
        self.init_var()
        self.init_ui()
        self.thread = GraphTMPThread(self.grafik, self.type_list)
        self.thread.s_error[str].connect(show_dlg_err)
        self.thread.start()
        # self.ComLine_init(path, type_data, freq)

    def __del__(self):
        self.thread.terminate = True

    def init_var(self):
        self.fpath = [None, None, None, None, None, None]
        self.fnames = [None, None, None, None, None, None]
        self.data_types = [None, None, None, None, None, None]
        self.freqs = [None, None, None, None, None, None]
        self.type_list = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32',
                          'double64']

    def init_ui(self):
        self.gbox_files = []
        self.btn_open_files = []
        self.combo_d_types = []
        self.lbl_d_types = []
        self.lbl_freq = []
        self.lbl_path = []
        self.spin_freq = []
        for i in range(6):
            self.gbox_files.append(QGroupBox('Файл №' + str(i + 1)))

            self.btn_open_files.append(QPushButton('Файл ...'))
            self.btn_open_files[-1].resize(self.btn_open_files[-1].sizeHint())
            self.btn_open_files[-1].clicked.connect(self.show_dlg_path)
            self.btn_open_files[-1].setStatusTip('Выбор файла №' + str(i + 1))

            self.lbl_path.append(QLabel(''))
            self.lbl_path[-1].setMinimumWidth(150)
            self.lbl_path[-1].setWordWrap(True)
            self.lbl_path[-1].setMaximumWidth(300)

            self.lbl_d_types.append(QLabel('Тип данных'))
            self.combo_d_types.append(QComboBox(self))
            self.combo_d_types[-1].setMinimumWidth(60)
            self.combo_d_types[-1].setStatusTip('Выберите тип данных')
            self.combo_d_types[-1].addItems(self.type_list)
            self.combo_d_types[-1].activated.connect(self.update_set_graph)

            self.lbl_freq.append(QLabel('Частота дискретизации'))
            self.spin_freq.append(QDoubleSpinBox(self))
            self.spin_freq[-1].setMinimumWidth(80)
            self.spin_freq[-1].setMaximumWidth(80)
            self.spin_freq[-1].setSingleStep(0.1)
            self.spin_freq[-1].setMaximum(32000.0)
            self.spin_freq[-1].setMinimum(0.00001)
            self.spin_freq[-1].setValue(100.0)
            self.spin_freq[-1].setDecimals(5)
            self.spin_freq[-1].editingFinished.connect(self.update_set_graph)
            self.spin_freq[-1].setStatusTip('Введите частоту дискретизации ТМП')

        self.gbox_setting = QGroupBox('Настройка отображения графиков')
        self.gbox_graph = []
        self.lbl_graph1 = []
        self.lbl_graph2 = []
        self.combo_graph1 = []
        self.combo_graph2 = []
        self.lbl_link1 = []
        self.lbl_link2 = []
        self.check_link1 = []
        self.check_link2 = []
        for i in range(3):
            self.gbox_graph.append(QGroupBox('Вкладка №' + str(i + 1)))
            self.lbl_graph1.append(QLabel('<font color="blue">Синий график</font>'))
            self.lbl_graph2.append(QLabel('<font color="red">Красный график</font>'))
            self.combo_graph1.append(QComboBox(self))
            self.combo_graph1[-1].setMinimumWidth(100)
            self.combo_graph1[-1].setStatusTip('Выберите загруженный файл')
            self.combo_graph1[-1].addItem('')
            self.combo_graph1[-1].activated.connect(self.update_set_graph)
            self.combo_graph2.append(QComboBox(self))
            self.combo_graph2[-1].setMinimumWidth(100)
            self.combo_graph2[-1].setStatusTip('Выберите загруженный файл')
            self.combo_graph2[-1].addItem('')
            self.combo_graph2[-1].activated.connect(self.update_set_graph)
            list_ = [x for x in range(3)]
            del list_[i]
            self.lbl_link1.append(QLabel('Связать ось X c вкладкой №' + str(list_[0] + 1)))
            self.lbl_link2.append(QLabel('Связать ось X c вкладкой №' + str(list_[1] + 1)))
            self.check_link1.append(QCheckBox())
            self.check_link1[-1].setChecked(False)
            self.check_link1[-1].stateChanged.connect(self.update_set_graph)
            self.check_link2.append(QCheckBox())
            self.check_link2[-1].setChecked(False)
            self.check_link2[-1].stateChanged.connect(self.update_set_graph)

        # График
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.grafik = DockArea()

        # Управление макетом
        self.cur_layout = self.layout_init()
        self.setLayout(self.cur_layout)

    def show_dlg_path(self):
        index = self.btn_open_files.index(self.sender())
        dir_path = '..'
        dlg_files = QFileDialog()
        dlg_files.setFileMode(QFileDialog.AnyFile)
        dlg_files.setLabelText(QFileDialog.LookIn, 'Выберите файл ТМП ...')
        dlg_files.setAcceptMode(QFileDialog.AcceptOpen)
        dlg_files.setDirectory(dir_path)
        if dlg_files.exec_():
            dir_, self.fnames[index] = os.path.split(dlg_files.selectedFiles()[0])
            self.lbl_path[index].setText(self.fnames[index])
            self.fpath[index] = dlg_files.selectedFiles()[0]
            self.update_set_graph()

    def update_set_graph(self):
        # Комбо на вкладках
        for i1 in range(3):
            temp = self.combo_graph1[i1].currentText()
            while self.combo_graph1[i1].count() > 0:
                self.combo_graph1[i1].removeItem(0)
            cur_index = 0
            fix_index = 0
            self.combo_graph1[i1].addItem('')
            for fname in self.fnames:
                if fname is None:
                    continue
                if self.combo_graph2[i1].currentText() != fname:
                    self.combo_graph1[i1].addItem(fname)
                    cur_index += 1
                if temp == fname:
                    fix_index = cur_index
            self.combo_graph1[i1].setCurrentIndex(fix_index)

        for i2 in range(3):
            temp = self.combo_graph2[i2].currentText()
            while self.combo_graph2[i2].count() > 0:
                self.combo_graph2[i2].removeItem(0)
            cur_index = 0
            fix_index = 0
            self.combo_graph2[i2].addItem('')
            for fname in self.fnames:
                if fname is None:
                    continue
                if self.combo_graph1[i2].currentText() != fname:
                    self.combo_graph2[i2].addItem(fname)
                    cur_index += 1
                if temp == fname:
                    fix_index = cur_index
            self.combo_graph2[i2].setCurrentIndex(fix_index)

        # Частоты дискретизации и типы данных
        for i in range(6):
            self.data_types[i] = self.combo_d_types[i].currentText()
            self.freqs[i] = self.spin_freq[i].value()
        # Формирование предустановок
        fpath = [None, None, None, None, None, None]
        data_types = [None, None, None, None, None, None]
        freqs = [None, None, None, None, None, None]
        links = [False, False, False, False, False, False]
        for i in range(3):
            if self.combo_graph1[i].currentText() != '':
                fpath[i * 2] = self.fpath[self.fnames.index(self.combo_graph1[i].currentText())]
            if self.combo_graph2[i].currentText() != '':
                fpath[i * 2 + 1] = self.fpath[self.fnames.index(self.combo_graph2[i].currentText())]
            if self.check_link1[i].isChecked():
                links[i * 2] = True
            else:
                links[i * 2] = False
            if self.check_link2[i].isChecked():
                links[i * 2 + 1] = True
            else:
                links[i * 2 + 1] = False
        for i in range(6):
            if fpath[i] is not None:
                data_types[i] = self.data_types[i]
                freqs[i] = self.freqs[i]
        self.thread.update_data(fpath, data_types, freqs, links)

    def layout_init(self):
        vbox_left = QVBoxLayout()
        # Настройка файлов
        for i in range(6):
            lay_vbox_open_file = QVBoxLayout()
            lay_vbox_open_file.addWidget(self.btn_open_files[i])
            lay_vbox_open_file.addWidget(self.lbl_path[i])

            lay_vbox_data_type = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.lbl_d_types[i])
            hbox.addStretch(1)
            lay_vbox_data_type.addLayout(hbox)
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.combo_d_types[i])
            hbox.addStretch(1)
            lay_vbox_data_type.addLayout(hbox)

            lay_vbox_freq = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.lbl_freq[i])
            hbox.addStretch(1)
            lay_vbox_freq.addLayout(hbox)
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.spin_freq[i])
            hbox.addStretch(1)
            lay_vbox_freq.addLayout(hbox)

            lay_hbox_file = QHBoxLayout()
            lay_hbox_file.addLayout(lay_vbox_open_file)
            lay_hbox_file.addLayout(lay_vbox_data_type)
            lay_hbox_file.addLayout(lay_vbox_freq)
            self.gbox_files[i].setLayout(lay_hbox_file)
            self.gbox_files[i].setMaximumWidth(450)

            vbox_left.addWidget(self.gbox_files[i])

        # Настройка графиков
        lay_vbox_setting = QVBoxLayout()
        for i in range(3):
            lay_vbox_select_graph1 = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.lbl_graph1[i])
            hbox.addStretch(1)
            lay_vbox_select_graph1.addLayout(hbox)
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.combo_graph1[i])
            hbox.addStretch(1)
            lay_vbox_select_graph1.addLayout(hbox)

            lay_vbox_select_graph2 = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.lbl_graph2[i])
            hbox.addStretch(1)
            lay_vbox_select_graph2.addLayout(hbox)
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.combo_graph2[i])
            hbox.addStretch(1)
            lay_vbox_select_graph2.addLayout(hbox)

            lay_hbox_link1 = QHBoxLayout()
            lay_hbox_link1.addWidget(self.lbl_link1[i])
            lay_hbox_link1.addWidget(self.check_link1[i])
            lay_hbox_link2 = QHBoxLayout()
            lay_hbox_link2.addWidget(self.lbl_link2[i])
            lay_hbox_link2.addWidget(self.check_link2[i])
            lay_vbox_link = QVBoxLayout()
            lay_vbox_link.addLayout(lay_hbox_link1)
            lay_vbox_link.addLayout(lay_hbox_link2)

            lay_hbox_vkladka = QHBoxLayout()
            lay_hbox_vkladka.addLayout(lay_vbox_select_graph1)
            lay_hbox_vkladka.addLayout(lay_vbox_select_graph2)
            lay_hbox_vkladka.addLayout(lay_vbox_link)

            self.gbox_graph[i].setLayout(lay_hbox_vkladka)

            lay_vbox_setting.addWidget(self.gbox_graph[i])

        self.gbox_setting.setLayout(lay_vbox_setting)
        self.gbox_setting.setMaximumWidth(450)

        vbox_left.addWidget(self.gbox_setting)
        vbox_left.addStretch(1)

        # График
        hbox_stretch = QHBoxLayout()
        hbox_stretch.addStretch(1)
        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.grafik)
        vbox_right.addLayout(hbox_stretch)
        # Итоговый layout
        hbox_common = QHBoxLayout()
        hbox_common.addLayout(vbox_left)
        hbox_common.addLayout(vbox_right)
        return hbox_common


def show_dlg_err(err):
    dlg_err = QMessageBox()
    dlg_err.setIcon(QMessageBox.Warning)
    dlg_err.setWindowTitle('Ошибка')
    dlg_err.setText(err + '\nВыберите новый файл.')
    dlg_err.setStandardButtons(QMessageBox.Ok)
    dlg_err.exec_()



"""
    def com_line_init(self, path, num_order, sign, freq):
        # Донастройка параметров командной строки
        if path is None or num_order is None or sign is None or freq is None:
            return
        self.fpath[0] = path
        self.num_orders[0] = num_order
        self.signs[0] = sign
        self.freqs[0] = freq
        # запуск задачи
        self.start_SBitChange_thread()
"""