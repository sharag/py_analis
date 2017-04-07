#!/usr/bin/python3.5
from AIS.ais_data_base import AISdb
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

db = AISdb('\\\\Fs37\\extra\\projects\\aisparser\\python\\linux\\ais_db.sqlite3')
slot_int_len = 60/2250
tab = db.get_time()
tab_slot = db.get_offset(tab[0])
slot_x = [tab_slot[i][1] // slot_int_len for i in range(len(tab_slot))]
tab = [tab_slot[i][1] % slot_int_len for i in range(len(tab_slot))]

#for slot in tab:



app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)
# Список окон
doc_graph = None
w_graph_slot = pg.PlotWidget(title='Распределение количества mmsi по слотам')
w_graph_slot.showGrid(x=False, y=True)
pen = pg.mkPen(color='b')
w_graph_slot.plot(y=tab, x=slot_x, pen=pen)
d_graph_slot = Dock('Распределение количества mmsi по слотам', size=(500, 300), closable=False)
d_graph_slot.addWidget(w_graph_slot)
area_graph = DockArea()
area_graph.addDock(d_graph_slot)

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
