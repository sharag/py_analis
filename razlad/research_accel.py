"""
Модуль исследования разладки
"""

import pyqtgraph as pg
import numpy as np
from razlad.functions import FormSurge, f_probability_dyach, f_probability
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import struct


app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# Данные
# Открываем файл режимов
in_fid = open('e:\\git\\signals\\1', mode='rb')
data_raw = in_fid.read()
#in_fid.close()
# Преобразуем к установленному формату
#if len(data_raw) % 2 == 0:
#    data = np.fromstring(data_raw, dtype=np.int16)
#else:
#    data = np.fromstring(data_raw[0:-1], dtype=np.int16)
#del data_raw
data = [0] * (len(data_raw) // 2)
for i in range(1, len(data_raw), 2):
    data[(i - 1) / 2] = struct.unpack('h', data_raw[i - 1:i])
del data_raw

# Параметры разладки
# tresholds = 200  # Порог отношения правдоподобия
bef_win_len = 160  # длина окна до скачка
aft_win_len = small_win_len_d = 40  # длина малого окна (и для классики и для варианта Дяченко)
great_win_len_d = bef_win_len + small_win_len_d  # Длина всего окна для варианта Дяченко

# Вычисление функции разладки
prob = f_probability(data, bef_win_len, aft_win_len)
prob_d = f_probability_dyach(data, great_win_len_d, small_win_len_d)

# Список окон
doc_win = None
# Графика
# Создадим графики и добавим их во вкладки
# График скачка
pen = pg.mkPen(color='b')
graph_surge = pg.PlotWidget(title='График скачка')
graph_surge.plot(y=data, pen=pen)
graph_surge.showGrid(x=False, y=True)

# График отношения правдоподобия
graph_prob = pg.PlotWidget(title='График отношения правдободобия')
pen1 = pg.mkPen(color='r')
pen2 = pg.mkPen(color='b')
x_axis = np.linspace(bef_win_len, len(data) - aft_win_len, len(data) - bef_win_len - aft_win_len)
plot_klass = graph_prob.plot(y=prob, x=x_axis, pen=pen1, name='Классика')
plot_dyach = graph_prob.plot(y=prob_d, x=x_axis, pen=pen2, name='Дяченко')
graph_prob.showGrid(x=False, y=True)
graph_prob.setXLink(graph_surge)
# graph_prob.addLegend()
leg = pg.LegendItem((90, 40), offset=(50, 10))
leg.addItem(plot_klass, 'Классика')
leg.addItem(plot_dyach, 'Дяченко')
leg.setParentItem(graph_prob.graphicsItem())

# Создадим вкладки и добавим их на окошко
d_graph_surge = Dock('График скачка', size=(500, 300), closable=False)
d_graph_surge.addWidget(graph_surge)
d_graph_prob = Dock('График отношения правдободобия', size=(500, 300), closable=False)
d_graph_prob.addWidget(graph_prob)
area = DockArea()
area.addDock(d_graph_surge)
area.addDock(d_graph_prob)
# Сформируем окошко
doc_win = QtGui.QMainWindow()
doc_win.resize(800, 800)
doc_win.setCentralWidget(area)
doc_win.setWindowTitle('Скачок из данных')
# Показываем виджет
doc_win.show()


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
