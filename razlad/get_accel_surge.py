import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import scipy.signal as sp_sig
from os import path
#from pyqtgraph.Point import Point

app = QtGui.QApplication([])
# Настройка графика
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

modes = []
# Открываем файл режимов
in_fid = open('e:\\fedorenko_ns\\work\\telemetry\\trident\\07.03.98\\work_D\\param\\T2-1d.bit.11.D1', mode='rb')
data_raw = in_fid.read()
# Преобразуем к установленному формату
if len(data_raw) % 2 == 0:
    data_mode = np.fromstring(data_raw, dtype=np.uint16)
else:
    data_mode = np.fromstring(data_raw[0:-1], dtype=np.uint16)
del data_raw
# Наложение битовой маски и битовое смещение вправо
for i in range(len(data_mode)):
    data_mode[i] = (data_mode[i] & 63488) >> 11
# Медианная фильтрация для устранения сбоев
data_mode = sp_sig.medfilt(data_mode, 5)
for i in range(1, len(data_mode)):
    if data_mode[i] != data_mode[i - 1]:
        modes.append([i, data_mode[i]])

# Открываем файл
in_fid = open('e:\\fedorenko_ns\\work\\telemetry\\trident\\07.03.98\\work_A\\T2-1a.bit.Ai0', mode='rb')
data_raw = in_fid.read()
# Преобразуем к установленному формату
if len(data_raw) % 2 == 0:
    data = np.fromstring(data_raw, dtype=np.int16)
else:
    data = np.fromstring(data_raw[0:-1], dtype=np.int16)
del data_raw
# Медианная фильтрация для устранения сбоев
data = sp_sig.medfilt(data, 5)

x_axis = np.linspace(0, len(data)/400, len(data))
# Строим график
graph_accel = pg.PlotWidget(title='График ускорения')
pen = pg.mkPen(color='b')
graph_accel.plot(y=data, x=x_axis, pen=pen)
graph_accel.showGrid(x=False, y=True)
region = pg.LinearRegionItem()
region.setZValue(10)
region.setRegion([len(data)/10/400, len(data)*2/10/400])
graph_accel.addItem(region, ignoreBounds=True)

for i in range(len(modes)):
    a = pg.ArrowItem()
    a.setPos(modes[i][0] / 100, data[modes[i][0] * 4])
    text = pg.TextItem(html='<div style="text-align: center">' + str(modes[i][1]) + '</div>', border='w',
                       fill=(0, 0, 255, 100))
    text.setPos(modes[i][0] / 100, data[modes[i][0] * 4])
    graph_accel.addItem(text)
    graph_accel.addItem(a)

# Создадим вкладки и добавим их на окошко
d_graph = Dock('График ускорения', size=(500, 300), closable=False)
layout = pg.LayoutWidget()
layout.addWidget(graph_accel, row=0, col=0)
saveBtn = QtGui.QPushButton('Save')


# Функция сохранения выбранного фрагмента
def save_file():
    minX, maxX = region.getRegion()
    n = 1
    while True:
        name = 'e:\\git\\signals\\' + str(n)
        if path.exists(name):
            n += 1
            continue
        else:
            break
    f_id = open(name, mode='wb')
    f_id.write(data[int(minX * 400), int(maxX * 400)])

saveBtn.clicked.connect(save_file)
layout.addWidget(saveBtn, row=1, col=0)
#d_graph.addWidget(graph_accel)
d_graph.addWidget(layout)
area = DockArea()
area.addDock(d_graph)

# Сформируем окошко
doc_win = QtGui.QMainWindow()
doc_win.resize(800, 800)
doc_win.setCentralWidget(area)
doc_win.setWindowTitle('График ускорения')
# Показываем виджет
doc_win.show()


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    """Исполняемая часть"""
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
