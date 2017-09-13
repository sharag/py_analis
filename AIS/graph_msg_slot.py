#!/usr/bin/python3.5
from AIS.ais_data_base import AISdb
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

slot_intervals = [time for time in np.linspace(0, 60, 2251, endpoint=True)]
db = AISdb('\\\\Fs37\\extra\\projects\\aisparser\\python\\linux\\ais_db.sqlite3')
tab = []
for slot_ind in range(len(slot_intervals) - 1):
    slot = db.get_slots(slot_intervals[slot_ind], slot_intervals[slot_ind + 1])
    mmsi = []
    mmsi_str = ''
    if len(slot) > 0:
        for i in range(len(slot)):
            if not slot[i][0] in mmsi:
                mmsi.append(slot[i][0])
                mmsi_str += str(slot[i][0]) + ', '
        tab.append(len(mmsi))
    else:
        tab.append(0)
    print('Slot: ' + str(slot_ind) + '. Number mmsi: ' + str(len(mmsi)) + '. MMSI: ' + mmsi_str)


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
w_graph_slot.plot(y=tab, pen=pen)
#pen = pg.mkPen(color='r')
#y, x = np.histogram(np.array(tab), bins=np.linspace(0, 2250, 2250, endpoint=True))
#w_graph_slot.plot(y=y, x=x, pen=pen)
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
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
