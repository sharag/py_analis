from PyQt5.QtCore import QThread, pyqtSignal
import os
import numpy as np
import pyqtgraph as pg
import scipy.signal as sp_sig


class GraphTMPThread(QThread):
    s_error = pyqtSignal(str)
    s_mode = pyqtSignal(list)

    def __init__(self, fname, num_order, w_grafik):
        super().__init__()
        self.fname = fname
        self.in_fid = None
        self.num_order = num_order
        self.grafik = w_grafik
        if not os.path.exists(fname):
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
