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
    pen_PO = pg.mkPen(color='b', width=2)
    pen_LT = pg.mkPen(color='r', width=2)
    pen_PC = pg.mkPen(color='g', width=2)
    graph_ver = pg.PlotWidget(title='Вероятностные характеристики обнаружения скачков')
    plot_PO = graph_ver.plot(y=cur_surge['PO'],
                             x=cur_surge['p_osh_array'],
                             pen=pen_PO,
                             name='Вероятность ПО')
    plot_LT = graph_ver.plot(y=cur_surge['LT'],
                             x=cur_surge['p_osh_array'],
                             pen=pen_LT,
                             name='Вероятность ЛТ')
    plot_PC = graph_ver.plot(y=cur_surge['PC'],
                             x=cur_surge['p_osh_array'],
                             pen=pen_PC,
                             name='Вероятность ПЦ')
    graph_ver.showGrid(x=False, y=True)

    leg = pg.LegendItem((90, 40), offset=(50, 10))
    leg.addItem(plot_PO, 'Вероятность ПО')
    leg.addItem(plot_LT, 'Вероятность ЛТ')
    leg.addItem(plot_PC, 'Вероятность ПЦ')
    leg.setParentItem(graph_ver.graphicsItem())

    graph_PO = pg.PlotWidget(title='График вероятности правильного обнаружения')
    graph_PO.plot(y=cur_surge['PO'],
                  x=cur_surge['p_osh_array'],
                  pen=pen_PO,
                  name='Вероятность ПО')
    graph_LT = pg.PlotWidget(title='График вероятности ложной тревоги')
    graph_LT.plot(y=cur_surge['LT'],
                  x=cur_surge['p_osh_array'],
                  pen=pen_LT,
                  name='Вероятность ЛТ')
    graph_PC = pg.PlotWidget(title='График вероятности пропуска цели')
    graph_PC.plot(y=cur_surge['PC'],
                   x=cur_surge['p_osh_array'],
                   pen=pen_PC,
                   name='Вероятность ПЦ')

    d_graph_ver = Dock(cur_surge['name'], size=(500, 300), closable=False)
    d_graph_ver.addWidget(graph_ver)
    d_graph_PO = Dock(cur_surge['name'] + ': вероятность правильного обнаружения', size=(500, 300), closable=False)
    d_graph_PO.addWidget(graph_PO)
    d_graph_LT = Dock(cur_surge['name'] + ': вероятность ложной тревоги', size=(500, 300), closable=False)
    d_graph_LT.addWidget(graph_LT)
    d_graph_PC = Dock(cur_surge['name'] + ': вероятность пропуска цели', size=(500, 300), closable=False)
    d_graph_PC.addWidget(graph_PC)
    area = DockArea()
    area.addDock(d_graph_ver)
    area.addDock(d_graph_PO)
    area.addDock(d_graph_LT)
    area.addDock(d_graph_PC)
    # Сформируем окошко
    doc_win = QtGui.QMainWindow()
    doc_win.resize(800, 800)
    doc_win.setCentralWidget(area)
    doc_win.setWindowTitle("Вероятностные характеристики")
    # Показываем виджет
    doc_win.show()

if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
