"""
Модуль исследования разладки
"""

import pyqtgraph as pg
import numpy as np
from razlad.functions import FormSurge, f_probability_dyach, f_probability
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *


app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# Данные
form_surge = FormSurge()
# Параметры разладки
# tresholds = 200  # Порог отношения правдоподобия
bef_win_len = 160  # длина окна до скачка
aft_win_len = small_win_len_d = 40  # длина малого окна (и для классики и для варианта Дяченко)
great_win_len_d = bef_win_len + small_win_len_d  # Длина всего окна для варианта Дяченко

# Список окон
doc_win = [None] * form_surge.num_surge

# Циклическое получение скачков, вычисление разладки и построение графиков
for k in range(form_surge.num_surge):

    #if k != 6:
        #continue
    # Получение временного ряда со скачком
    # data, data_name, surge_list, surge_prop = form_surge.get_surge(None, bef_win_len + aft_win_len)
    data, data_name, surge_list, surge_prop = form_surge.get_surge(k, bef_win_len + aft_win_len)

    # Вычисление функции разладки
    prob = f_probability(data, bef_win_len, aft_win_len)
    prob_d = f_probability_dyach(data, great_win_len_d, small_win_len_d)

    # Графика
    # Создадим графики и добавим их во вкладки
    # График скачка
    pen = pg.mkPen(color='b')
    graph_surge = pg.PlotWidget(title='График скачка')
    graph_surge.plot(y=data, pen=pen)
    graph_surge.showGrid(x=False, y=True)
    if surge_list is not None:
        for m in range(len(surge_list)):
            text = pg.TextItem(html='<div style="text-align: center">' + str(surge_prop[m]) + '</div>')
            # text = pg.TextItem(html='<div style="text-align: center">Ширина ' + str(surge_prop[m]) + '</div>',
            #                    anchor=(-0.3, 0.5), angle=0, border='k', fill=(0, 0, 255, 100))
            graph_surge.addItem(text)
            text.setPos(surge_list[m], 1.2)

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

    # Создадим вкладки и добавим из на окошко
    d_graph_surge = Dock('График скачка', size=(500, 300), closable=False)
    d_graph_surge.addWidget(graph_surge)
    d_graph_prob = Dock('График отношения правдободобия', size=(500, 300), closable=False)
    d_graph_prob.addWidget(graph_prob)
    area = DockArea()
    area.addDock(d_graph_surge)
    area.addDock(d_graph_prob)
    # Сформируем окошко
    doc_win[k] = QtGui.QMainWindow()
    doc_win[k].resize(800, 800)
    doc_win[k].setCentralWidget(area)
    doc_win[k].setWindowTitle(data_name)
    # Показываем виджет
    doc_win[k].show()


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
