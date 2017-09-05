"""
Модуль исследования разладки
"""

import pyqtgraph as pg
import numpy as np
from rsch_razlad.functions import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import pickle


app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# Характеристики исследования
null_len = 200  # длина холостого участка
k_surge = 0.1  # Коэффициент отношения длины временного ряда к длине скачка
surge_len = int(null_len*k_surge)  # Длина скачка
step_win = 10  # Шаг изменения окна минимум 2
num_order = 16  # Количество разрядов отсчетов для учета вероятности ошибки
num_test = 10  # Количество экспериментов для каждого значения вероятности ошибки

# Массив вероятностей ошибок
p_osh_array = np.linspace(0.0001, 0.001, 25)
p_osh_array = np.append(p_osh_array, np.linspace(0.001, 0.01, 25))
p_osh_array = np.append(p_osh_array, np.linspace(0.01, 0.06, 10))
p_osh_array = p_osh_array*num_order


def post_sost():
    """Исследование скачка постоянной составляющей"""
    # Скачок постоянной составляющей
    surge_ps, surge_ps_index = get_post_sost(null_len, surge_len, 1)

    # Определим оптимальные параметры окна и порог
    win, win_bef, win_aft, max_prob_val = optimum_win_param(surge_ps, step_win)
    porog = 0.9 * max_prob_val

    print("\n\nОптимальные параметры окна для скачка постоянной составляющей:")
    print("До скачка: %d отсчетов" % win_bef)
    print("После скачка: %d отсчетов" % win_aft)
    print("Окно: %d отсчетов" % win)
    print("Максимум функции отношения правдоподобия: %d" % max_prob_val)
    print("Порог функции отношения правдоподобия: %d" % int(porog))

    # График функции отношения правдоподобия с оптимальным окном
    prob = f_probability(surge_ps, win_bef, win_aft)

    # Определение веоятностных характеристик
    print("\n\nОпределение вероятностных характеристик")
    num_po = list()
    num_lt = list()
    num_pc = list()
    i = 0
    for p_osh in p_osh_array:
        i += 1
        print('\rtest:' + str(i) + '/' + str(len(p_osh_array)), end='')
        num_po_, num_lt_, num_pc_ = test_probability(num_test, surge_ps, win_bef, win_aft, porog, surge_ps_index, p_osh)
        num_po.append(num_po_)
        num_lt.append(num_lt_)
        num_pc.append(num_pc_)
    num_po = np.array(num_po)/num_test
    num_lt = np.array(num_lt)/num_test
    num_pc = np.array(num_pc)/num_test
    return surge_ps, prob, num_po, num_lt, num_pc, [win, win_bef, win_aft, porog]

surges = []
surges.append(post_sost())

with open('e:\\git\\data\\razlad\\surge_ps', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(surges[0], f, pickle.HIGHEST_PROTOCOL)

pen_surge = pg.mkPen(color='b',
                     width=2)
pen_prob = pg.mkPen(color='r',
                    width=2)
pen_porog = pg.mkPen(color='g',
                     width=2)
graph_surge = pg.PlotWidget(title='Скачок и функция отношения правдоподобия')
surge = [i*int(0.7*surges[0][5][3]) for i in surges[0][0]]


plot_surge = graph_surge.plot(y=[i*int(0.95*surges[0][5][3]) for i in surges[0][0]],
                              pen=pen_surge,
                              name='Скачок')
x_axis_prob = np.linspace(surges[0][5][1], len(surges[0][0]) - surges[0][5][2], len(surges[0][1]))
plot_prob = graph_surge.plot(y=surges[0][1],
                             x=x_axis_prob,
                             pen=pen_prob,
                             name='Функция отношения правдоподобия')
plot_porog = graph_surge.plot(y=[surges[0][5][3]] * len(surges[0][0]),
                              x=np.linspace(0, len(surges[0][0]), len(surges[0][0])),
                              pen=pen_porog,
                              name='Порог')
graph_surge.showGrid(x=False, y=True)

leg = pg.LegendItem((90, 40), offset=(50, 10))
leg.addItem(plot_surge, 'Скачок')
leg.addItem(plot_prob, 'Функция ОП')
leg.addItem(plot_porog, 'Порог')
leg.setParentItem(graph_surge.graphicsItem())

d_graph_surge = Dock('График скачка и функции ОП с порогом', size=(500, 300), closable=False)
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

"""

    if surge_list is not None:
        for m in range(len(surge_list)):
            text = pg.TextItem(html='<div style="text-align: center">' + str(surge_prop[m]) + '</div>')
            # text = pg.TextItem(html='<div style="text-align: center">Ширина ' + str(surge_prop[m]) + '</div>',
            #                    anchor=(-0.3, 0.5), angle=0, border='k', fill=(0, 0, 255, 100))
            graph_surge.addItem(text)
            text.setPos(surge_list[m], 1.2)
            
            
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
"""



# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
