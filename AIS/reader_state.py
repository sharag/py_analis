#!/usr/bin/python3.5
import sys
import argparse
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import copy
import numpy as np


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    return parser_


def sort_2_list(x_list, y_list):
    x_out = []
    y_out = []
    temp = []
    for index in range(len(x_list)):
        temp.append([x_list[index], y_list[index]])
    temp.sort()
    for pos in temp:
        x_out.append(pos[0])
        y_out.append(pos[1])
    return x_out, y_out

app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)
# Список окон
doc_graph = None
doc_mesh = None

parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])
inpath = namespace.inpath[0]
if len(namespace.inpath) > 1:
    for i in range(1, len(namespace.inpath)):
        inpath += ' ' + namespace.inpath[i]
namespace.inpath = inpath
del inpath
fid_in = open(namespace.inpath, 'r')
array_pll_gain = []
array_in_lpf = []
array_dc_lpf = []
array_num_mes = []
# Чтение массива
for line in fid_in:
    if line.find('Current') >= 0:
        array_pll_gain.append(float(line.split('\t')[1].split(':')[1]))
        array_in_lpf.append(float(line.split('\t')[2].split(':')[1]))
        array_dc_lpf.append(float(line.split('\t')[3].split(':')[1]))
        array_num_mes.append(float(line.split('\t')[4].split(':')[1]))
fid_in.close()

w_graph_in_lpf = pg.PlotWidget(title='Зависимость количества демодулированных сообщений от in_lpf')
w_graph_in_lpf.showGrid(x=False, y=True)
w_graph_dc_lpf = pg.PlotWidget(title='Зависимость количества демодулированных сообщений от dc_lpf')
w_graph_dc_lpf.showGrid(x=False, y=True)
w_graph_pll_gain = pg.PlotWidget(title='Зависимость количества демодулированных сообщений от pll_gain')
w_graph_pll_gain.showGrid(x=False, y=True)

copy_array = list(array_num_mes)
ind_max_list = []
old_max = 0
for num in range(100):
    # Определение параметров
    index_max = array_num_mes.index(max(copy_array))
    if max(copy_array) == old_max and index_max in ind_max_list:
        index_max = array_num_mes[(ind_max_list[-1] + 1):].index(max(copy_array)) + ind_max_list[-1] + 1
    ind_max_list.append(index_max)
    copy_array[ind_max_list[-1]] = 0
    old_max = max(copy_array)
    good_pll_gain = array_pll_gain[index_max]
    good_in_lpf = array_in_lpf[index_max]
    good_dc_lpf = array_dc_lpf[index_max]

    # Формирование осей для графиков
    # По dc_lpf
    indexes_pll_gain = [i for i, x in enumerate(array_pll_gain) if x == good_pll_gain]
    indexes_in_lpf = [x for x in indexes_pll_gain if array_in_lpf[x] == good_in_lpf]
    x_dc_lpf = [array_dc_lpf[x] for x in indexes_in_lpf]
    y_dc_lpf = [array_num_mes[x] for x in indexes_in_lpf]
    x_dc_lpf, y_dc_lpf = sort_2_list(x_dc_lpf, y_dc_lpf)

    # По in_lpf
    indexes_pll_gain = [i for i, x in enumerate(array_pll_gain) if x == good_pll_gain]
    indexes_dc_lpf = [x for x in indexes_pll_gain if array_dc_lpf[x] == good_dc_lpf]
    x_in_lpf = [array_in_lpf[x] for x in indexes_dc_lpf]
    y_in_lpf = [array_num_mes[x] for x in indexes_dc_lpf]
    x_in_lpf, y_in_lpf = sort_2_list(x_in_lpf, y_in_lpf)

    # По pll_gain
    indexes_in_lpf = [i for i, x in enumerate(array_in_lpf) if x == good_in_lpf]
    indexes_dc_lpf = [x for x in indexes_in_lpf if array_dc_lpf[x] == good_dc_lpf]
    x_pll_gain = [array_pll_gain[x] for x in indexes_dc_lpf]
    y_pll_gain = [array_num_mes[x] for x in indexes_dc_lpf]
    x_pll_gain, y_pll_gain = sort_2_list(x_pll_gain, y_pll_gain)

    # Графика
    # Создадим графики и добавим их во вкладки
    # График pll_gain
    pen = pg.mkPen(color='g')
    w_graph_pll_gain.plot(y=y_pll_gain, x=x_pll_gain, pen=pen)
    # График in_lpf
    pen = pg.mkPen(color='r')
    w_graph_in_lpf.plot(y=y_in_lpf, x=x_in_lpf, pen=pen)

    # График dc_lpf
    pen = pg.mkPen(color='b')
    w_graph_dc_lpf.plot(y=y_dc_lpf, x=x_dc_lpf, pen=pen)

# Собираем графики
d_graph_demod = Dock('Количество демодулированных сообщений', size=(500, 300), closable=False)
d_graph_demod.addWidget(w_graph_dc_lpf)
d_graph_demod.addWidget(w_graph_in_lpf)
d_graph_demod.addWidget(w_graph_pll_gain)
area_graph = DockArea()
area_graph.addDock(d_graph_demod)

doc_graph = QtGui.QMainWindow()
doc_graph.resize(800, 800)
doc_graph.setCentralWidget(area_graph)
doc_graph.setWindowTitle('Исследование демодулятора')
# Показываем виджет
doc_graph.show()

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
