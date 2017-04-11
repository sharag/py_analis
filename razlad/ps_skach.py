import numpy as np
import matplotlib.pyplot as plt
from razlad.functions import max_probabil, f_probability, test_probability

num_order = 16
# Характеристики скачков
graph_len = 600
k_surge = 0.1
surge_len = int(graph_len*k_surge)
# Характеристики окна
win_size = 250
step_win = 2  # минимум 2

num_test = 1000
# Скачок
surge_ps = [0]*((graph_len - surge_len)//2)
surge_ps.extend([1]*surge_len)
surge_ps.extend([0]*int((graph_len - surge_len)/2))
# График скачка
signal = surge_ps
plt.figure(40)
plt.subplot(1, 1, 1)
plt.plot(signal, linewidth=3)
plt.grid(True)
plt.show()
# Определим оптимальные параметры окна и порог
len_win, len_win_bef, probabl_x2_ps_obr = max_probabil(surge_ps, win_size, surge_len, step_win)
max_ind = list()
max_ind.append(np.argmax(probabl_x2_ps_obr)//probabl_x2_ps_obr.shape[1])
max_ind.append(np.argmax(probabl_x2_ps_obr) % probabl_x2_ps_obr.shape[1])
win = len_win[max_ind[0]]
win_bef = len_win_bef[max_ind[1]]
win_aft = win - win_bef
porog = 0.9*np.max(probabl_x2_ps_obr)
# График функции отношения правдоподобия с оптимальным окном
prob = f_probability(surge_ps, win_bef, win_aft)
plt.figure(41)
plt.subplot(1, 1, 1)
x_axis = np.linspace(win_bef, len(surge_ps) - win_aft, len(surge_ps) - win_bef - win_aft)
plt_prob, = plt.plot(x_axis, prob, linewidth=3)
plt_porog, = plt.plot(x_axis, [porog]*len(x_axis), linewidth=3)
plt.legend([plt_prob, plt_porog], [r'$\Lambda$', r'$0.9 * \max(\Lambda)$'])
plt.grid(True)
plt.show()
# Добавили шумов
indexes_skach = [(graph_len//2 - surge_len) + i for i in range(surge_len * 2)]
p_osh_array = np.linspace(0.0001, 0.001, 25)
p_osh_array = np.append(p_osh_array, np.linspace(0.001, 0.01, 30))
p_osh_array = np.append(p_osh_array, np.linspace(0.01, 0.06, 5))
p_osh_array = p_osh_array*num_order
num_po = list()
num_lt = list()
num_pc = list()
i = 0
for p_osh in p_osh_array:
    i += 1
    print('test:' + str(i) + '/' + str(len(p_osh_array)))
    num_po_, num_lt_, num_pc_ = test_probability(num_test, surge_ps, win_bef, win_aft, porog, indexes_skach, p_osh)
    num_po.append(num_po_)
    num_lt.append(num_lt_)
    num_pc.append(num_pc_)
num_po = np.array(num_po)
num_lt = np.array(num_lt)
num_pc = np.array(num_pc)

plt.figure(42)
plt.subplot(1, 1, 1)
plt.plot(np.array(p_osh_array), num_po/num_test, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(43)
plt.subplot(1, 1, 1)
plt.plot(np.array(p_osh_array), num_lt/num_test, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(44)
plt.subplot(1, 1, 1)
plt.plot(np.array(p_osh_array), num_pc/num_test, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(45)
plt.subplot(1, 1, 1)
plt.plot(np.array(p_osh_array), (num_lt + num_pc)/num_test, linewidth=3)
plt.grid(True)
plt.show()
