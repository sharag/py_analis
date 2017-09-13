#!/usr/bin/python3.5
import sys
import argparse
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import glob
import os
import copy
import numpy as np


def create_parser():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument('-i', '--inpath', nargs='+', help='Path to the input directory: -i <path>')
    parser.add_argument('-r', '--recursive', nargs='?', help='Search recursive in input directory: -r', default=False)
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

#parser = create_parser()
#namespace = parser.parse_args(sys.argv[1:])
#inpath = namespace.inpath[0]
#if len(namespace.inpath) > 1:
#    for i in range(1, len(namespace.inpath)):
#        inpath += ' ' + namespace.inpath[i]
#namespace.inpath = inpath
#del inpath

#print(os.path.exists(namespace.inpath))
#filesList = glob.glob(namespace.inpath + '**/*.iq', recursive=True)
#print(namespace.inpath + '**/*.iq')
#print('\n'.join(filesList))

inpath = 'e:\\New folder\\'
print(os.path.exists(inpath))
filesList = glob.glob(inpath + '**/*.dat', recursive=True)
print(inpath + '**/*.iq')
print('\n'.join(filesList))

per = []
p_sig = []
for file in filesList:
    fid_in = open(file, 'rb')
    data = fid_in.read()
    fid_in.close()
    data = data.decode('cp1251')

    data = data[20:]
    if len(data)//2:
        data = data[:-1]
        print('Нечетное число бит.')

    num_err = 0
    meta = False
    for i in range(1, len(data)):
        if meta:
            if data[i - 1] != data[i]:
                num_err += 1
            else:
                meta = False
        else:
            if data[i - 1] == data[i]:
                num_err += 1
                meta = True

    if num_err > len(data)//2:
        num_err = len(data) - num_err

    per.append(num_err/len(data))
    p_sig.append(int(file.split('_')[1].split('.')[0]) * 0.000001)


w_graph = pg.PlotWidget(title='Зависимость вероятности ошибки от амплитуды входного сигнала')
w_graph.showGrid(x=False, y=True)
pen = pg.mkPen(color='r')
w_graph.plot(y=per, x=p_sig, pen=pen)
d_graph = Dock('Зависимость вероятности ошибки от амплитуды входного сигнала', size=(500, 300), closable=False)
d_graph.addWidget(w_graph)
area_graph = DockArea()
area_graph.addDock(d_graph)

doc_graph = QtGui.QMainWindow()
doc_graph.resize(800, 800)
doc_graph.setCentralWidget(area_graph)
doc_graph.setWindowTitle('Исследование чувствительности приемника')
# Показываем виджет
doc_graph.show()

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
