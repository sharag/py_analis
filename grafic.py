import pyqtgraph as pg
import numpy as np
from razlad.functions import FormSurge
from pyqtgraph.Qt import QtCore, QtGui

# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# p5.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
# p5.setLabel('left', "Y Axis", units='A')
# p5.setLabel('bottom', "Y Axis", units='s')
# p5.setLogMode(x=True, y=False)

# Формирование окошка
grafik_win = pg.GraphicsWindow(title=data_name)
grafik_win.setWindowTitle(data_name)

# График сигнала
pen = pg.mkPen(color='b')
graph_surge = grafik_win.addPlot(y=data, title='График скачка', pen=pen, name='graph_surge')
graph_surge.showGrid(x=False, y=True)

# График отношения правдободобия
grafik_win.nextRow()
pen = pg.mkPen(color='r')
x_axis = np.linspace(great_win_len - small_win_len, len(data) - small_win_len, len(data) - great_win_len)
graph_prob = grafik_win.addPlot(y=prob, x=x_axis, title='График отношения правдободобия', pen=pen, name='graph_prob')
graph_prob.showGrid(x=False, y=True)
graph_prob.setXLink('graph_surge')

# График МО большого окна
grafik_win.nextRow()
pen = pg.mkPen(color='g')
x_axis = np.linspace(great_win_len/2, len(data) - great_win_len/2, len(data) - great_win_len)
title = 'График МО большого окна'
graph_mo_great = grafik_win.addPlot(y=mo_great, x=x_axis, title=title, pen=pen, name='graph_mo_great')
graph_mo_great.showGrid(x=False, y=True)
graph_mo_great.setXLink('graph_surge')

# График МО малого окна
grafik_win.nextRow()
pen = pg.mkPen(color='c')
x_axis = np.linspace(great_win_len - small_win_len/2, len(data) - small_win_len/2, len(data) - great_win_len)
graph_mo_small = grafik_win.addPlot(y=mo_small, x=x_axis, title='График МО малого окна', pen=pen, name='graph_mo_small')
graph_mo_small.showGrid(x=False, y=True)
graph_mo_small.setXLink('graph_surge')

# График дисперсии большого окна
grafik_win.nextRow()
pen = pg.mkPen(color='m')
x_axis = np.linspace(great_win_len/2, len(data) - great_win_len/2, len(data) - great_win_len)
title = 'График дисперсии большого окна'
graph_disp_great = grafik_win.addPlot(y=dispers_great, x=x_axis, title=title, pen=pen, name='graph_disp_great')
graph_disp_great.showGrid(x=False, y=True)
graph_disp_great.setXLink('graph_surge')










# График
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.grafik = pg.PlotWidget(name='Plot1')
        self.grafik.setLabel('left', '<font size="5">Амплитуда</font>')
        # self.grafik.setLabel('bottom', '<font size="5">Время, (c)</font>', units='с')
        self.grafik.setLabel('bottom', '<font size="5">Время, (c)</font>')
        # self.grafik.setXRange(0, 2)
        # self.grafik.setYRange(0, 1e-10)


self.grafik.clear()  # Очищение графика
        pen_ = pg.mkPen(color='b')
        self.grafik.plot(y=data, x=np.linspace(0.01, len(data) * 0.01, len(data)), pen=pen_)