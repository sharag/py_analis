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

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
d_graph_surge = []
area = DockArea()
pen_PO = pg.mkPen(color='b', width=2)
pen_LT = pg.mkPen(color='r', width=2)
pen_PC = pg.mkPen(color='g', width=2)
d_graph_ver = []
graph_PO = pg.PlotWidget(title='График вероятности правильного обнаружения')
graph_LT = pg.PlotWidget(title='График вероятности ложной тревоги')
graph_PC = pg.PlotWidget(title='График вероятности пропуска цели')
leg_list = []
graph_ver_list = []
plot_PO_list = []
plot_LT_list = []
plot_PC_list = []
leg_PO = pg.LegendItem((90, 40), offset=(50, 10))
leg_LT = pg.LegendItem((90, 40), offset=(50, 10))
leg_PC = pg.LegendItem((90, 40), offset=(50, 10))
for cur_surge in surges:
    graph_ver_list.append(pg.PlotWidget(title=cur_surge['name']))
    plot_PO = graph_ver_list[-1].plot(y=cur_surge['PO'],
                                      x=cur_surge['p_osh_array'],
                                      pen=pen_PO,
                                      name='Вероятность ПО')
    plot_LT = graph_ver_list[-1].plot(y=cur_surge['LT'],
                                      x=cur_surge['p_osh_array'],
                                      pen=pen_LT,
                                      name='Вероятность ЛТ')
    plot_PC = graph_ver_list[-1].plot(y=cur_surge['PC'],
                                      x=cur_surge['p_osh_array'],
                                      pen=pen_PC,
                                      name='Вероятность ПЦ')
    graph_ver_list[-1].showGrid(x=False, y=True)

    leg_list.append(pg.LegendItem((90, 40), offset=(50, 10)))
    leg_list[-1].addItem(plot_PO, 'Вероятность ПО')
    leg_list[-1].addItem(plot_LT, 'Вероятность ЛТ')
    leg_list[-1].addItem(plot_PC, 'Вероятность ПЦ')
    leg_list[-1].setParentItem(graph_ver_list[-1].graphicsItem())

    d_graph_ver.append(Dock(cur_surge['name'], size=(500, 300), closable=False))
    d_graph_ver[-1].addWidget(graph_ver_list[-1])
    area.addDock(d_graph_ver[-1])

    pen = pg.mkPen(color=colors[len(plot_PO_list)], width=2)
    plot_PO_list.append(graph_PO.plot(y=cur_surge['PO'],
                                      x=cur_surge['p_osh_array'],
                                      pen=pen,
                                      name=cur_surge['name']))
    leg_PO.addItem(plot_PO_list[-1], cur_surge['name'])
    plot_LT_list.append(graph_LT.plot(y=cur_surge['LT'],
                                      x=cur_surge['p_osh_array'],
                                      pen=pen,
                                      name=cur_surge['name']))
    leg_LT.addItem(plot_LT_list[-1], cur_surge['name'])
    plot_PC_list.append(graph_PC.plot(y=cur_surge['PC'],
                                      x=cur_surge['p_osh_array'],
                                      pen=pen,
                                      name=cur_surge['name']))
    leg_PC.addItem(plot_PC_list[-1], cur_surge['name'])

leg_PO.setParentItem(graph_PO.graphicsItem())
leg_LT.setParentItem(graph_LT.graphicsItem())
leg_PC.setParentItem(graph_PC.graphicsItem())

d_graph_PO = Dock('Вероятность правильного обнаружения', size=(500, 300), closable=False)
d_graph_PO.addWidget(graph_PO)
d_graph_LT = Dock('Вероятность ложной тревоги', size=(500, 300), closable=False)
d_graph_LT.addWidget(graph_LT)
d_graph_PC = Dock('Вероятность пропуска цели', size=(500, 300), closable=False)
d_graph_PC.addWidget(graph_PC)


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
