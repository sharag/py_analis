import scipy.signal as sp_sig
import numpy as np
import matplotlib.pyplot as plt
import copy
from razlad.functions import max_probabil, f_probability, test_probability

num_order = 16
step_mode = 10

modes = []
# Открываем файл режимов
#in_fid = open('d:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.11.D1', mode='rb')
in_fid = open('e:\\fedorenko_ns\\work\\telemetry\\trident\\07.03.98\\work_D\\param\\T2-1d.bit.11.D1', mode='rb')
data_raw = in_fid.read()
# Преобразуем к установленному формату
if len(data_raw) % 2 == 0:
    data_mode_temp = np.fromstring(data_raw, dtype=np.uint16)
else:
    data_mode_temp = np.fromstring(data_raw[0:-1], dtype=np.uint16)
del data_raw
data_mode = []
for ind in range(0, len(data_mode_temp), step_mode):
    data_mode.append(data_mode_temp[ind])
del data_mode_temp
# Наложение битовой маски и битовое смещение вправо
for i in range(len(data_mode)):
    data_mode[i] = (data_mode[i] & 63488) >> 11
# Медианная фильтрация для устранения сбоев
data_mode = sp_sig.medfilt(data_mode, 5)
for i in range(1, len(data_mode)):
    if data_mode[i] != data_mode[i - 1]:
        modes.append([i, data_mode[i]])

# Открываем файл
# Файлы с угловыми скоростями
fnames = [0, 0, 0]
#fnames[0] = 'd:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.44.D4'
#fnames[1] = 'd:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.46.D4'
#fnames[2] = 'd:\\work\\signals\\GTS\\07.03.98\\workD\\T2-1d.bit.47.D4'
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

plt.figure(1)
plt.subplot(1, 1, 1)
plt.plot(data[2], linewidth=2)
plt.plot(data_mode*500, linewidth=2)
plt.grid(True)
plt.show()

# Поиск скачков и сохранение индексов
indexes_skach = [[0, []], [0, []], [0, []]]
porogs = [500, 2500, 500]
for i in range(3):
    k = 0
    while True:
        if k >= len(data[i]):
            break
        if abs(data[i][k]) <= porogs[i]:
            k += 1
            continue
        else:
            indexes_skach[i][0] += 1
            while abs(data[i][k]) > porogs[i]:
                if k >= len(data[i]):
                    break
                indexes_skach[i][1].append(k)
                k += 1
summ_skach = sum([indexes_skach[i][0] for i in range(3)])

# сделаем график, в котором вне скачка все равно 0
graph = copy.copy(data)
for i in range(3):
    for k in range(len(data[i])):
        if k not in indexes_skach[i][1]:
            graph[i][k] = 0
plt.figure(2)
plt.subplot(1, 1, 1)
plt.plot(data[2], linewidth=2)
plt.plot(graph[2], linewidth=2)
plt.grid(True)
plt.show()
