import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
"""
Для работы необходимо задать путь к файлу с сохраненнными скачками в формате 'razladka':

surges.append({'name': 'Импульс с квадратическим изменением значений',
               'surge': surge,
               'prob': prob,
               'PO': po,
               'LT': lt,
               'PC': pc,
               'p_osh_array': p_osh_array,
               'surf': {'surf': max_prob_surf,
                        'x': len_win_bef_x,
                        'y': len_win_aft_y},
               'opt': {'win': win,
                       'win_bef': win_bef,
                       'win_aft': win_aft,
                       'porog': porog}})
"""
# Путь к файлу со скачками
path = 'e:\\git\\data\\razlad\\surge'


with open(path, 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    surges = pickle.load(f)


d_graph_surge = []
grid = []
widg = []
plot = []

for cur_surge in surges:
    x, y = np.meshgrid(cur_surge['surf']['x'], cur_surge['surf']['y'])
    # скачок постоянной составляющей
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    # Plot the surface.
    surf = ax.plot_surface(x, y, cur_surge['surf']['surf'], cmap=cm.seismic, linewidth=2,
                           antialiased=True)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # ax.xaxis(len_win_x)
    ax.set_xlabel('Окно до скачка')
    ax.set_ylabel('Окно после скачка')
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
"""
    widg.append(gl.GLViewWidget())
    widg[-1].show()
    widg[-1].setWindowTitle('Выбор параметров окна по максимуму функции ОП')
    widg[-1].setCameraPosition(distance=50)
    widg[-1].addItem(grid[-1])
    plot.append(gl.GLSurfacePlotItem(x=cur_surge['surf']['x'],
                                     y=cur_surge['surf']['y'],
                                     # z=cur_surge['surf']['surf'], shader='shaded', color=(0.5, 0.5, 1, 1)))
                                     z=cur_surge['surf']['surf'],  shader='normalColor'))
    #plot[-1].scale(16. / 49., 16. / 49., 1.0)
    plot[-1].scale(1.0, 1.0, 1.0)
    plot[-1].translate(-18, 2, 0)
    widg[-1].addItem(plot[-1])

    d_graph_surge.append(Dock(cur_surge['name'], size=(500, 300), closable=False))
    d_graph_surge[-1].addWidget(widg[-1])

    area.addDock(d_graph_surge[-1])

# Сформируем окошко
doc_win = QtGui.QMainWindow()
doc_win.resize(800, 800)
doc_win.setCentralWidget(area)
doc_win.setWindowTitle("График скачка и функции ОП")
# Показываем виджет
doc_win.show()

if __name__ == '__main__':
    import sys
    '''Исполняемая часть'''
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
"""
