"""
Модуль исследования разладки
"""

import pyqtgraph as pg
import numpy as np
from razlad.get_surge import FormSurge
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *


def f_probability(data_, before_win_len, after_win_len):
    """ Функция вычисления отношения правдоподобия
    data_ - входной массив, тип list
    before_win_len - длина окна до скачка
    after_win_len - длина окна после скачка"""
    # Формирование массива для хранения значений отношения правдободобия скользящего окна
    probability = [0] * (len(data_) - before_win_len - after_win_len)
    for i in range(len(data_) - before_win_len - after_win_len):
        # Математическое ожидание окна до скачка
        mean_before = np.mean(data_[i:i + before_win_len])
        # Математическое ожидание окна после скачка
        mean_after = np.mean(data_[i + before_win_len:i + before_win_len + after_win_len])
        # Дисперсия окна обоих окон
        var_all = np.var(data_[i:i + before_win_len + after_win_len])
        if var_all == 0:
            var_all = 0.000000001
        # Подсчет суммы для отношения правдободобия
        summ = 0
        for j in range(after_win_len):
            summ += data_[i + before_win_len + j] - mean_before - (mean_after - mean_before) / 2
        # Расчет отношения правдоподобия
        probability[i] = (mean_after - mean_before)*summ/var_all
    return probability


def f_probability_dyach(data_, gr_win_len, sm_win_len):
    """ Функция вычисления отношения правдоподобия
    data_ - входной массив, тип list
    gr_win_len - длина большого окна
    sm_win_len - длина малого окна"""
    # Формирование массива для хранения значений отношения правдободобия скользящего окна
    probability = [0] * (len(data_) - gr_win_len)
    for i in range(len(data_) - gr_win_len):
        # Математическое ожидание всего окна
        mean_great = np.mean(data_[i:i + gr_win_len])
        # Математическое ожидание малого окна (после скачка)
        mean_small = np.mean(data_[i + gr_win_len - sm_win_len:i + gr_win_len])
        # Дисперсия всего окна
        var_all = np.var(data_[i:i + gr_win_len])
        if var_all == 0:
            var_all = 0.000000001
        # Подсчет суммы для отношения правдободобия
        summ = 0
        for j in range(sm_win_len):
            summ += data_[i + gr_win_len - sm_win_len + j] - mean_great - (mean_small - mean_great) / 2
        # Расчет отношения правдоподобия
        probability[i] = (mean_small - mean_great)*summ/var_all

    return probability

app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# Данные
razladka = FormSurge()
# Параметры разладки
# tresholds = 200  # Порог отношения правдоподобия
bef_win_len = 160  # длина окна до скачка
aft_win_len = small_win_len_d = 40  # длина малого окна (и для классики и для варианта Дяченко)
great_win_len_d = bef_win_len + small_win_len_d  # Длина всего окна для варианта Дяченко

# Список окон
doc_win = [None] * razladka.num_surge

# Циклическое получение скачков, вычисление разладки и построение графиков
for k in range(razladka.num_surge):

    # Получение временного ряда со скачком
    data, data_name = razladka.get_surge()

    # Вычисление функции разладки
    prob = f_probability(data, bef_win_len, aft_win_len)
    prob_d = f_probability_dyach(data, great_win_len_d, small_win_len_d)

    # Графика
    # Сформируем окошко
    doc_win[k] = QtGui.QMainWindow()
    doc_win[k].resize(800, 800)
    area = DockArea()
    doc_win[k].setCentralWidget(area)
    doc_win[k].setWindowTitle(data_name)
    # Создадим вкладки и добавим из на окошко
    d_graph_surge = Dock('График скачка', size=(500, 300), closable=False)
    d_graph_prob = Dock('График отношения правдободобия', size=(500, 300), closable=False)
    area.addDock(d_graph_surge)
    area.addDock(d_graph_prob)

    # Создадим графики и добавим их во вкладки
    graph_surge = pg.PlotWidget(title='График скачка')
    pen = pg.mkPen(color='b')
    graph_surge.plot(y=data, pen=pen)
    graph_surge.showGrid(x=False, y=True)
    d_graph_surge.addWidget(graph_surge)

    graph_prob = pg.PlotWidget(title='График отношения правдободобия')
    leg = pg.LegendItem((90, 40), offset=(50, 10))
    leg.setParentItem(graph_prob.graphicsItem())
    pen = pg.mkPen(color='r')
    x_axis = np.linspace(bef_win_len, len(data) - aft_win_len, len(data) - bef_win_len - aft_win_len)
    plot_klass = graph_prob.plot(y=prob, x=x_axis, pen=pen, name='Классика')
    pen = pg.mkPen(color='b')
    plot_dyach = graph_prob.plot(y=prob_d, x=x_axis, pen=pen, name='Дяченко')
    graph_prob.showGrid(x=False, y=True)
    graph_prob.setXLink(graph_surge)
    # graph_prob.addLegend()
    leg.addItem(plot_klass, 'Классика')
    leg.addItem(plot_dyach, 'Дяченко')
    d_graph_prob.addWidget(graph_prob)

    # Показываем виджет
    doc_win[k].show()


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
