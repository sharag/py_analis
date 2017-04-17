#!/usr/bin/python3.5
from AIS.ais_data_base import AISdb
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

db = AISdb('\\\\Fs37\\extra\\projects\\aisparser\\python\\linux\\ais_db.sqlite3')
slot_int_len = 60/2250
kadr_list = db.get_time()
num_kadr = 30
offset = []
slot_num = []
mmsi = []
for i in range(num_kadr):
    tab_slot = db.get_offset(kadr_list[i])
    for j in range(len(tab_slot)):
        add_sign = False
        for k in range(len(offset)):
            if (slot_num[k] * slot_int_len) + offset[k] >= tab_slot[j][1]:
                offset.insert(k, ((tab_slot[j][1]) % slot_int_len)) # % (48/9600)
                slot_num.insert(k, tab_slot[j][1] // slot_int_len)
                mmsi.insert(k, tab_slot[j][0])
                if offset[k] > 0.004:
                    print('mmsi: ' + str(mmsi[k]) + '\toffset:' + str(offset[k]) + '\tslot_num:' + str(slot_num[k]))
                add_sign = True
                break
        if not add_sign:
            offset.append((tab_slot[j][1] % (48 / 9600)) % slot_int_len)
            slot_num.append(tab_slot[j][1] // slot_int_len)
            mmsi.append(tab_slot[j][0])
            if offset[-1] > 0.004:
                print('mmsi: ' + str(mmsi[-1]) + '\toffset:' + str(offset[-1]) + '\tslot_num:' + str(slot_num[-1]))

delta = []
for i in range(1, len(offset)):
    delta.append(abs(offset[i] - offset[i-1]))

del kadr_list


# tab = [tab_slot[i][1] % slot_int_len for i in range(len(tab_slot))]
# Устранили 48 бит


#for slot in tab:



app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)
# Список окон
doc_graph = None
w_graph_slot = pg.PlotWidget(title='Смещение начала сообщения относительно границ слота')
w_graph_slot.showGrid(x=False, y=True)
pen = pg.mkPen(color='b')
w_graph_slot.plot(y=offset, x=slot_num, pen=pen)
d_graph_slot = Dock('Смещение начала сообщения относительно границ слота', size=(500, 300), closable=False)
d_graph_slot.addWidget(w_graph_slot)

w_graph_delta = pg.PlotWidget(title='Модуль разности смещений')
w_graph_delta.showGrid(x=False, y=True)
pen = pg.mkPen(color='r')
w_graph_delta.plot(y=delta, x=slot_num[1:], pen=pen)
w_graph_delta.setXLink(w_graph_slot)
d_graph_delta = Dock('Модуль разности смещений', size=(500, 300), closable=False)
d_graph_delta.addWidget(w_graph_delta)

area_graph = DockArea()
area_graph.addDock(d_graph_slot)
area_graph.addDock(d_graph_delta)

doc_graph = QtGui.QMainWindow()
doc_graph.resize(800, 800)
doc_graph.setCentralWidget(area_graph)
doc_graph.setWindowTitle('Исследование слотов')
# Показываем виджет
doc_graph.show()

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    '''Исполняемая часть'''
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
