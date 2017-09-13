import scipy.signal as sp_sig
import numpy as np
import matplotlib.pyplot as plt
from razlad.functions import max_probabil, f_probability, test_probability

num_order = 16
step_mode = 10

# Открываем файл
# Файлы с угловыми скоростями
fnames = [0, 0, 0]
# fnames[0] = 'd:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.44.D4'
# fnames[1] = 'd:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.46.D4'
# fnames[2] = 'd:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.47.D4'
fnames[0] = 'e:\\fedorenko_ns\\work\\telemetry\\trident\\07.03.98\\work_D\\param\\T2-1d.bit.44.D4'
fnames[1] = 'e:\\fedorenko_ns\\work\\telemetry\\trident\\07.03.98\\work_D\\param\\T2-1d.bit.46.D4'
fnames[2] = 'e:\\fedorenko_ns\\work\\telemetry\\trident\\07.03.98\\work_D\\param\\T2-1d.bit.47.D4'
data = np.array([[0]*10907, [0]*10907, [0]*10907])
i = 0
for fname in fnames:
    fid = open(fname, mode='rb')
    data_raw = fid.read()
    fid.close()
    # Преобразуем к установленному формату
    if len(data_raw) % 2 == 0:
        data_temp = np.fromstring(data_raw, dtype=np.int16)
    else:
        data_temp = np.fromstring(data_raw[0:-1], dtype=np.int16)
    data_ = []
    for ind in range(0, len(data_temp), step_mode):
        data_.append(data_temp[ind])
    del data_temp
    # Медианная фильтрация для устранения сбоев
    data[i][0:len(data_)] = sp_sig.medfilt(data_, 5)
    i += 1
    del data_
    del data_raw
#plt.figure(11)
#plt.subplot(1, 1, 1)
#plt.plot(data[0], linewidth=2)
#plt.plot(data_mode*500, linewidth=2)
#plt.grid(True)
#plt.show()

# Поиск скачков и сохранение индексов
indexes_skach = [[0, []], [0, []], [0, []]]
porogs = [650, 2500, 1500]
begin_sig = 1800
end_sig = 8250
for i in range(3):
    k = begin_sig
    while True:
        if k >= end_sig:
            break
        if abs(data[i][k]) <= porogs[i]:
            k += 1
            continue
        else:
            indexes_skach[i][0] += 1
            while abs(data[i][k]) > porogs[i]:
                if k >= end_sig:
                    break
                indexes_skach[i][1].append(k)
                k += 1
summ_skach = sum([indexes_skach[i][0] for i in range(3)])
# Определим оптимальные параметры скользящего окна
step_win = 10
#win_begin = 160
#win_size = 600
# len_win_array = np.arange(win_begin, win_size, step_win)
len_win = 600
win_bef_array = np.arange(300, 600, 10)
num_po = list()
num_lt = list()
num_pc = list()
p_osh = 0
num_test = 1
porog = 21
l = 0
for win_bef in win_bef_array:
    print('Exp:' + str(l + 1) + '/' + str(len(win_bef_array)))
    l += 1
    # win_bef = int(len_win*0.65)
    win_aft = len_win - win_bef
    num_po_mean = 0
    num_lt_mean = 0
    num_pc_mean = 0
    for i in range(3):
        num_po_, num_lt_, num_pc_ = test_probability(num_test, data[i][begin_sig:end_sig], win_bef, win_aft, porog, indexes_skach[i][1],
                                                     p_osh)
        num_po_mean += num_po_
        num_lt_mean += num_lt_
        num_pc_mean += num_pc_
        if num_po_mean > summ_skach:
            num_po_mean = summ_skach
        if num_lt_mean > summ_skach:
            num_lt_mean = summ_skach
        if num_pc_mean > summ_skach:
            num_pc_mean = summ_skach
    num_po.append(num_po_mean)
    num_lt.append(num_lt_mean)
    num_pc.append(num_pc_mean)
num_po = np.array(num_po)
num_lt = np.array(num_lt)
num_pc = np.array(num_pc)

plt.figure(12)
plt.subplot(1, 1, 1)
plt_po, = plt.plot(np.array(win_bef_array), num_po/summ_skach, linewidth=2)
plt_lt_pc, = plt.plot(np.array(win_bef_array), (num_lt + num_pc)/summ_skach, linewidth=2)
plt.legend([plt_po, plt_lt_pc], ['ПО', 'ЛТ+ПЦ'])
plt.grid(True)
plt.show()


# plt.figure(12)
# plt.subplot(1, 1, 1)
# plt.plot(np.array(win_bef_array), num_po/summ_skach, linewidth=3)
# plt.grid(True)
# plt.show()

# plt.figure(13)
# plt.subplot(1, 1, 1)
# plt.plot(np.array(win_bef_array), num_lt/summ_skach, linewidth=3)
# plt.grid(True)
# plt.show()

# plt.figure(14)
# plt.subplot(1, 1, 1)
# plt.plot(np.array(win_bef_array), num_pc/summ_skach, linewidth=3)
# plt.grid(True)
# plt.show()

# plt.figure(15)
# plt.subplot(1, 1, 1)
# plt.plot(np.array(win_bef_array), (num_lt + num_pc)/summ_skach, linewidth=3)
# plt.grid(True)
# plt.show()
print()
