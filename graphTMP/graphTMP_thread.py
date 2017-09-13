from PyQt5.QtCore import QThread, pyqtSignal
import os
from pyqtgraph.dockarea.Dock import DockLabel
from pyqtgraph.dockarea import *
from graphTMP.DockFed import DockFed
from pyqtgraph.Qt import QtCore
import time
import os
import numpy as np
import pyqtgraph as pg
import scipy.signal as sp_sig


class GraphTMPThread(QThread):
    s_error = pyqtSignal(str)
    s_mode = pyqtSignal(list)

    def __init__(self, grafik, type_list):
        super().__init__()
        self.terminate = False
        self.need_chng = False
        self.need_regraph1 = False
        self.need_regraph2 = False
        self.need_regraph3 = False
        self.fnames = [None, None, None, None, None, None]
        self.fnames_chng = [None, None, None, None, None, None]
        self.data_types = [None, None, None, None, None, None]
        self.data_types_chng = [None, None, None, None, None, None]
        self.freqs = [None, None, None, None, None, None]
        self.freqs_chng = [None, None, None, None, None, None]
        self.links = [False, False, False, False, False, False]
        self.links_chng = [False, False, False, False, False, False]
        self.type_list = type_list
        self.area = grafik
        self.w_graph_vkl1 = pg.PlotWidget(title='')
        self.w_graph_vkl1.showGrid(x=False, y=True)
        self.w_graph_vkl1.setLabel('left', '<font size="4">Амплитуда</font>')
        self.w_graph_vkl1.setLabel('bottom', '<font size="4">Время, (c)</font>')
        self.w_graph_vkl2 = pg.PlotWidget(title='')
        self.w_graph_vkl2.showGrid(x=False, y=True)
        self.w_graph_vkl2.setLabel('left', '<font size="4">Амплитуда</font>')
        self.w_graph_vkl2.setLabel('bottom', '<font size="4">Время, (c)</font>')
        self.w_graph_vkl3 = pg.PlotWidget(title='')
        self.w_graph_vkl3.showGrid(x=False, y=True)
        self.w_graph_vkl3.setLabel('left', '<font size="4">Амплитуда</font>')
        self.w_graph_vkl3.setLabel('bottom', '<font size="4">Время, (c)</font>')
        d_graph_demod1 = DockFed('Вкладка №1', size=(500, 300), closable=False)
        d_graph_demod2 = DockFed('Вкладка №2', size=(500, 300), closable=False)
        d_graph_demod3 = DockFed('Вкладка №3', size=(500, 300), closable=False)
        d_graph_demod1.addWidget(self.w_graph_vkl1)
        d_graph_demod2.addWidget(self.w_graph_vkl2)
        d_graph_demod3.addWidget(self.w_graph_vkl3)
        self.area.addDock(d_graph_demod1)
        self.area.addDock(d_graph_demod2)
        self.area.addDock(d_graph_demod3)

    def update_data(self, fnames, data_types, freqs, links):
        """В потоке проверяем, есть ли необходимость внесения изменений"""
        need_change = False
        self.fnames_chng = fnames
        self.data_types_chng = data_types
        self.freqs_chng = freqs
        self.links_chng = links
        for i in range(6):
            if self.fnames[i] != fnames[i]:
                need_change = True
                break
            if self.data_types[i] != data_types[i]:
                need_change = True
                break
            if self.freqs[i] != freqs:
                need_change = True
                break
            if self.links[i] != links[i]:
                need_change = True
                break
        if need_change:
            self.need_chng = True

    def run(self):
        """"""
        data_raw = [None, None, None, None, None, None]
        data = [None, None, None, None, None, None]
        x_axis = [None, None, None, None, None, None]
        while True:
            if self.terminate:
                break
            time.sleep(0.01)
            # Изменение файла
            if self.need_chng:
                # для смены файла
                for i in range(6):
                    if self.fnames[i] != self.fnames_chng[i]:
                        if i in [0, 1]:
                            self.need_regraph1 = True
                        elif i in [2, 3]:
                            self.need_regraph2 = True
                        elif i in [4, 5]:
                            self.need_regraph3 = True
                        self.fnames[i] = self.fnames_chng[i]
                        self.fnames_chng[i] = None
                        if self.fnames[i] is None:
                            self.data_types[i] = None
                            self.freqs[i] = None
                            if data[i] is not None:
                                np.delete(data[i], [x for x in range(len(data[i]))])
                            if data_raw[i] is not None:
                                data_raw[i] = []
                            if x_axis[i] is not None:
                                np.delete(x_axis[i], [x for x in range(len(x_axis[i]))])
                            continue
                        if data_raw[i] is not None:
                            del data_raw[i][:]
                        try:
                            in_fid = open(self.fnames[i], mode='rb')
                            data_raw[i] = in_fid.read()
                            in_fid.close()
                        except BaseException as err:
                            print(err)
                            self.s_error.emit(err)
                            break
                        # Изменение типа
                        if self.data_types[i] != self.data_types_chng[i]:
                            self.data_types[i] = self.data_types_chng[i]
                        if data[i] is not None:
                            np.delete(data[i], [x for x in range(len(data[i]))])
                        data[i] = get_type(data_raw[i], self.data_types[i], self.type_list)
                        # Ось X
                        if self.freqs[i] != self.freqs_chng[i]:
                            self.freqs[i] = self.freqs_chng[i]
                        if x_axis[i] is not None:
                            np.delete(x_axis[i], [x for x in range(len(x_axis[i]))])
                        x_axis[i] = np.linspace(1/self.freqs[i], len(data[i])/self.freqs[i], len(data[i]))

                # для изменения типа
                for i in range(6):
                    if self.data_types[i] != self.data_types_chng[i]:
                        if i in [0, 1]:
                            self.need_regraph1 = True
                        elif i in [2, 3]:
                            self.need_regraph2 = True
                        elif i in [4, 5]:
                            self.need_regraph3 = True
                        self.data_types[i] = self.data_types_chng[i]
                        if data[i] is not None:
                            np.delete(data[i], [x for x in range(len(data[i]))])
                        data[i] = get_type(data_raw[i], self.data_types[i], self.type_list)

                        # Ось X
                        if self.freqs[i] != self.freqs_chng[i]:
                            self.freqs[i] = self.freqs_chng[i]
                        if x_axis[i] is not None:
                            np.delete(x_axis[i], [x for x in range(len(x_axis[i]))])
                        x_axis[i] = np.linspace(1 / self.freqs[i], len(data[i]) / self.freqs[i], len(data[i]))

                # для изменения частоты дискретизации
                for i in range(6):
                    if self.freqs[i] != self.freqs_chng[i]:
                        if i in [0, 1]:
                            self.need_regraph1 = True
                        elif i in [2, 3]:
                            self.need_regraph2 = True
                        elif i in [4, 5]:
                            self.need_regraph3 = True
                        self.freqs[i] = self.freqs_chng[i]
                        if x_axis[i] is not None:
                            np.delete(x_axis[i], [x for x in range(len(x_axis[i]))])
                        x_axis[i] = np.linspace(1 / self.freqs[i], len(data[i]) / self.freqs[i], len(data[i]))

                # Строим графики
                if self.need_regraph1:
                    self.w_graph_vkl1.clear()
                    if data[0] is None and data[1] is None:
                        self.w_graph_vkl1.plot(y=[0, 0], x=[0, 1], pen=pg.mkPen(width=1, color='b'), name='1')
                        self.w_graph_vkl1.setXRange({0, 200})
                        self.need_regraph1 = False
                    if self.need_regraph1:
                        if data[0] is not None:
                            self.w_graph_vkl1.plot(y=data[0], x=x_axis[0], pen=pg.mkPen(width=1, color='b'), name='1')
                            #self.w_graph_vkl1.setXRange([0.0, 99.0])
                            print('1')
                        if data[1] is not None:
                            self.w_graph_vkl1.plot(y=data[1], x=x_axis[1], pen=pg.mkPen(width=1, color='r'), name='2')
                            #self.w_graph_vkl1.setXRange({0.0, 200.0}, padding=0.1)
                        self.w_graph_vkl1.enableAutoRange('y', 0.9)
                        self.need_regraph1 = False

                if self.need_regraph2:
                    self.w_graph_vkl2.clear()
                    if data[2] is None and data[3] is None:
                        self.w_graph_vkl2.plot(y=[0, 0], x=[0, 1], pen=pg.mkPen(width=1, color='b'), name='1')
                        #self.w_graph_vkl2.setXRange({0, 400})
                        self.need_regraph2 = False
                    if self.need_regraph2:
                        if data[2] is not None:
                            self.w_graph_vkl2.plot(y=data[2], x=x_axis[2], pen=pg.mkPen(width=1, color='b'), name='3')
                            #self.w_graph_vkl2.setXRange({0, 400})
                        if data[3] is not None:
                            self.w_graph_vkl2.plot(y=data[3], x=x_axis[3], pen=pg.mkPen(width=1, color='r'), name='4')
                            #self.w_graph_vkl2.setXRange({0, 400})
                        self.w_graph_vkl2.enableAutoRange('y', 0.9)
                        self.need_regraph2 = False

                if self.need_regraph3:
                    self.w_graph_vkl3.clear()
                    if data[4] is None and data[5] is None:
                        self.w_graph_vkl3.plot(y=[0, 0], x=[0, 1], pen=pg.mkPen(width=1, color='b'), name='1')
                        #self.w_graph_vkl3.setXRange({0, 400})
                        self.need_regraph3 = False
                    if self.need_regraph3:
                        if data[4] is not None:
                            self.w_graph_vkl3.plot(y=data[4], x=x_axis[4], pen=pg.mkPen(width=1, color='b'), name='1')
                            #self.w_graph_vkl3.setXRange({0, 400})
                        if data[5] is not None:
                            self.w_graph_vkl3.plot(y=data[5], x=x_axis[5], pen=pg.mkPen(width=1, color='r'), name='2')
                            #self.w_graph_vkl3.setXRange({0, 400})
                        self.w_graph_vkl3.enableAutoRange('y', 0.9)
                        self.need_regraph3 = False
                self.need_chng = False


def get_type(data_r, type_np, type_list):
    if type_np == type_list[0]:
        return np.fromstring(data_r, dtype=np.int8)
    if type_np == type_list[1]:
        return np.fromstring(data_r, dtype=np.uint8)
    if type_np == type_list[2]:
        len_data = len(data_r) // 2
        return np.fromstring(data_r[:(len_data * 2)], dtype=np.int16)
    if type_np == type_list[3]:
        len_data = len(data_r) // 2
        return np.fromstring(data_r[:(len_data * 2)], dtype=np.uint16)
    if type_np == type_list[4]:
        len_data = len(data_r) // 4
        return np.fromstring(data_r[:(len_data * 4)], dtype=np.int32)
    if type_np == type_list[5]:
        len_data = len(data_r) // 4
        return np.fromstring(data_r[:(len_data * 4)], dtype=np.uint32)
    if type_np == type_list[6]:
        len_data = len(data_r) // 8
        return np.fromstring(data_r[:(len_data * 8)], dtype=np.int64)
    if type_np == type_list[7]:
        len_data = len(data_r) // 8
        return np.fromstring(data_r[:(len_data * 8)], dtype=np.uint64)
    if type_np == type_list[8]:
        len_data = len(data_r) // 4
        return np.fromstring(data_r[:(len_data * 4)], dtype=np.float32)
    if type_np == type_list[9]:
        len_data = len(data_r) // 8
        return np.fromstring(data_r[:(len_data * 8)], dtype=np.double)

"""if not os.path.exists(fname):
            raise BaseException('File not exist.')

    def run(self):
        self.in_fid = open(self.fname, mode='rb')
        data_raw = self.in_fid.read()

        # Преобразуем к установленному формату
        if len(data_raw) % 2 == 0:
            data = np.fromstring(data_raw, dtype=np.uint16)
        else:
            data = np.fromstring(data_raw[0:-1], dtype=np.uint16)
        del data_raw

        # Наложение битовой маски и битовое смещение вправо
        for i in range(len(data)):
            data[i] = (data[i] & 63488) >> 11

        # Медианная фильтрация для устранения сбоев
        data = sp_sig.medfilt(data, 5)

        # Строим график
        #self.grafik.plot(y=data, x=np.linspace(0.01, len(data)*0.01, len(data)), pen=pg.mkPen(width=2, color='b'))
        self.grafik.clear()  # Очищение графика
        pen_ = pg.mkPen(color='b')
        self.grafik.plot(y=data, x=np.linspace(0.01, len(data) * 0.01, len(data)), pen=pen_)

        # Ищем режимы
        self.s_mode.emit([int(data[0]), 0])
        for i in range(1, len(data)):
            if data[i] != data[i - 1]:
                self.s_mode.emit([int(data[i]), i])


"""
