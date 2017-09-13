import pickle
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)




null_len = 100
surge_len = 20
skvaj = 1
x_array = np.linspace(np.pi, 3 * np.pi, surge_len)

surge = np.array([0] * int(null_len * skvaj))

surge = np.append(surge, [np.cos(x) + 1 for x in x_array])

surge = np.append(surge, ([0] * int(null_len * skvaj)))



pen_surge = pg.mkPen(color='b', width=2)
graph_surge = pg.PlotWidget(title='Скачок')
plot_surge = graph_surge.plot(y=surge,
                              pen=pen_surge,
                              name='Скачок')
graph_surge.showGrid(x=False, y=True)

d_graph_surge = Dock('Скачок', size=(500, 300), closable=False)
d_graph_surge.addWidget(graph_surge)
area = DockArea()
area.addDock(d_graph_surge)
# Сформируем окошко
doc_win = QtGui.QMainWindow()
doc_win.resize(800, 800)
doc_win.setCentralWidget(area)
doc_win.setWindowTitle("График скачка")
# Показываем виджет
doc_win.show()

if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
