import pickle
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

"""
Для работы необходимо задать путь к файлу с сохраненнными скачками в формате 'razladka':

surges.append({'name': 'surge_ps',
               'surge': surge,
               'prob': prob,
               'PO': num_po,
               'LT': num_lt,
               'PC': num_pc,
               'p_osh_array': p_osh_array,
               'opt': {'win': win,
                       'win_bef': win_bef,
                       'win_aft': win_aft,
                       'porog': porog}})
"""
# Путь к файлу со скачками
path = 'e:\\git\\data\\razlad\\surge'

app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

with open(path, 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    surges = pickle.load(f)

for cur_surge in surges:
    pen_surge = pg.mkPen(color='b', width=2)
    pen_prob = pg.mkPen(color='r', width=2)
    pen_porog = pg.mkPen(color='g', width=2)
    graph_surge = pg.PlotWidget(title='Скачок и функция отношения правдоподобия')
    plot_surge = graph_surge.plot(y=[i*int(0.95*cur_surge['opt']['porog']) for i in cur_surge['surge']],
                                  pen=pen_surge,
                                  name='Скачок')
    plot_prob = graph_surge.plot(y=cur_surge['prob'],
                                 x=np.linspace(cur_surge['opt']['win_bef'],
                                               len(cur_surge['surge']) - cur_surge['opt']['win_aft'],
                                               len(cur_surge['prob'])),
                                 pen=pen_prob,
                                 name='Функция отношения правдоподобия')
    plot_porog = graph_surge.plot(y=[cur_surge['opt']['porog']] * len(cur_surge['surge']),
                                  x=np.linspace(0, len(cur_surge['surge']), len(cur_surge['surge'])),
                                  pen=pen_porog,
                                  name='Порог')
    graph_surge.showGrid(x=False, y=True)

    leg = pg.LegendItem((90, 40), offset=(50, 10))
    leg.addItem(plot_surge, 'Скачок')
    leg.addItem(plot_prob, 'Функция ОП')
    leg.addItem(plot_porog, 'Порог')
    leg.setParentItem(graph_surge.graphicsItem())

    d_graph_surge = Dock(cur_surge['name'], size=(500, 300), closable=False)
    d_graph_surge.addWidget(graph_surge)
    area = DockArea()
    area.addDock(d_graph_surge)
    # Сформируем окошко
    doc_win = QtGui.QMainWindow()
    doc_win.resize(800, 800)
    doc_win.setCentralWidget(area)
    doc_win.setWindowTitle("График скачка и функции ОП")
    # Показываем виджет
    doc_win.show()

if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
