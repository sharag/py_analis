"""
Модуль формирования скачков
"""
import numpy as np
import copy


def get_post_sost(null_len, surge_len, skvaj):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками"""
    # 0
    surge_ps = [0] * null_len
    # 1
    surge_ps_indexes = [i for i in range(len(surge_ps), len(surge_ps) + surge_len)]
    surge_ps.extend([1] * surge_len)
    # 0
    surge_ps.extend([0] * int(null_len * skvaj))
    # 1
    surge_ps_indexes.extend([i for i in range(len(surge_ps), len(surge_ps) + surge_len)])
    surge_ps.extend([1] * surge_len)
    # 0
    surge_ps.extend([0] * int(null_len * skvaj))
    # 1
    surge_ps_indexes.extend([i for i in range(len(surge_ps), len(surge_ps) + surge_len)])
    surge_ps.extend([1] * surge_len)
    # 0
    surge_ps.extend([0] * null_len)
    return surge_ps, surge_ps_indexes


def get_post_sost_skvaj(graph_len, surge_len, skvaj):
    surge_ps = [0] * (graph_len // 2 - surge_len // 2)
    surge_ps_indexes = [i for i in range(len(surge_ps), len(surge_ps)+surge_len)]
    surge_ps.extend([1] * surge_len)
    surge_ps.extend([0] * (graph_len // 2 - surge_len // 2))
    return surge_ps, surge_ps_indexes


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


def optimum_win_param(signal, step_win):
    """Функция определения оптимальных размеров окна, участка до скачка и участка после скачка
    signal - входной временной ряд
    step_win - шаг изменения размера окна (четное)"""
    print("\nПоиск оптимальных параметров окна по максимуму функции отношения правдоподобия.")
    max_len_win = len(signal)  # Максимальный размер окна не превышает половины длины временного ряда
    len_win_cur = np.arange(step_win, max_len_win, step_win)  # Текущий размер окна
    len_win_bef = np.arange(int(step_win/2), max_len_win - int(step_win/2), int(step_win/2))  #
    max_prob = np.zeros([len(len_win_cur), len(len_win_bef)])
    numtest_win = len(len_win_cur)
    numtest_win_bef = len(len_win_bef)
    numtest = numtest_win * numtest_win_bef
    i = 0
    for len_win_ind in range(len(len_win_cur)):
        for len_win_bef_ind in range(len(len_win_bef)):
            if len_win_cur[len_win_ind] - len_win_bef[len_win_bef_ind] < 2:
                i += 1
                continue
            if len_win_bef[len_win_bef_ind] < len_win_cur[len_win_ind] // 2:
                i += 1
                continue
            len_win_aft = len_win_cur[len_win_ind] - len_win_bef[len_win_bef_ind]
            max_prob[len_win_ind][len_win_bef_ind] = \
                max(f_probability(signal, len_win_bef[len_win_bef_ind], len_win_aft))
            i += 1
            print('\rТест (%d : %d): %d/%d' % (numtest_win, numtest_win_bef, i, numtest), end='')
    max_ind = list()
    max_ind.append(np.argmax(max_prob) // max_prob.shape[1])
    max_ind.append(np.argmax(max_prob) % max_prob.shape[1])
    win = len_win_cur[max_ind[0]]
    win_bef = len_win_bef[max_ind[1]]
    win_aft = win - win_bef
    max_prob_val = np.max(max_prob)
    return win, win_bef, win_aft, max_prob_val


def add_nois(sig_, p):
    sig = copy.copy(sig_)
    if p == 0:
        return sig
    num_rand = int(round(len(sig)*p + 0.5))
    n_sample = np.random.randint(0, len(sig), num_rand)
    for i in range(len(n_sample)):
        sig[n_sample[i]] = np.random.random()
    return sig


def test_probability(num_test, insignal, win_bef, win_aft, porog, indexes_skach, p):

    if len(indexes_skach):
        num_skach = 1
    else:
        return
    for l in range(1, len(indexes_skach)):
        if indexes_skach[l] - indexes_skach[l-1] > 1:
            num_skach += 1
    num_po = 0  # Правильное обнаружение
    num_lt = 0  # Ложная тревога
    num_pc = 0  # Пропуск цели
    for i in range(num_test):  # Испытания
        signal = add_nois(insignal, p)
        prob = f_probability(signal, win_bef, win_aft)
        k = 0
        num_po_test = 0  # Правильное обнаружение
        num_lt_test = 0  # Ложная тревога
        num_pc_test = 0  # Пропуск цели
        while True:  # Проверяем превышение порога функцией правдоподобия
            if k >= (len(prob)-1):
                break
            if prob[k] < porog:
                k += 1
                continue
            else:  # Подсчитываем индексы значений функциии правдоподобия, превышающих порог
                indexes_prob = list()
                while prob[k] > porog:
                    if k >= (len(prob)-1):
                        break
                    indexes_prob.append(k + win_bef)
                    k += 1
                # Сверяем обнаруженные индексы с индексами скачка
                obn = False
                for ind in indexes_prob:
                    if ind in indexes_skach:
                        obn = True
                        break
                # принимаем решение: обнаружение или ложная тревога
                if obn:
                    num_po_test += 1
                else:
                    num_lt_test += 1
        if num_po_test < num_skach:
            num_pc_test = num_skach - num_po_test
        if num_po_test > num_skach:
            num_lt_test += num_po_test - num_skach
            num_po_test = num_skach
        num_po += num_po_test
        num_lt += num_lt_test
        num_pc += num_pc_test
    return num_po, num_lt, num_pc
