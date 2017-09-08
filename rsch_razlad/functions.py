"""
Модуль формирования скачков
"""
import numpy as np


def get_post_sost(null_len, surge_len, skvaj, n_surge):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками
    n_surge - количество скачков"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge

    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, [1] * surge_len)
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes


def get_lin(null_len, surge_len, skvaj, n_surge):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками
    n_surge - количество скачков"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge

    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, ([x / (surge_len / 2) for x in range(surge_len // 2)]))
        surge = np.append(surge, ([(1 - x / (surge_len / 2)) for x in range(surge_len // 2)]))
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes


def get_kvadr(null_len, surge_len, skvaj, n_surge):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками
    n_surge - количество скачков"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge

    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, [((x / (surge_len / 4)) ** 2) / 2 for x in range(surge_len // 4)])
        surge = np.append(surge,
                          [(1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5 for x in range(surge_len // 4)])
        surge = np.append(surge, [1 - (((x / (surge_len / 4)) ** 2) / 2) for x in range(surge_len // 4)])
        surge = np.append(surge,
                          [1 - ((1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5)
                           for x in range(surge_len // 4)])
        surge = np.append(surge, ([0] * int(null_len * skvaj)))
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes


def get_high_cos(null_len, surge_len, skvaj, n_surge):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками
    n_surge - количество скачков"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge
    x_array = np.linspace(np.pi, 3 * np.pi, surge_len)
    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, [np.cos(x) + 1 for x in x_array])
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes


def research_surge(surge_ps, surge_ps_index, step_win, koef_porog_, num_test, p_osh_array, n_surge):
    """Исследование скачка постоянной составляющей"""

    # Определим оптимальные параметры окна и порог
    win_, win_bef_, win_aft, max_prob_val = optimum_win_param(surge_ps, step_win)
    porog_ = koef_porog_ * max_prob_val

    print("\n\nОптимальные параметры окна для скачка постоянной составляющей:")
    print("До скачка: %d отсчетов" % win_bef_)
    print("После скачка: %d отсчетов" % win_aft)
    print("Окно: %d отсчетов" % win_)
    print("Максимум функции отношения правдоподобия: %d" % max_prob_val)
    print("Порог функции отношения правдоподобия: %d" % int(porog_))

    # График функции отношения правдоподобия с оптимальным окном
    prob_ = f_probability(surge_ps, win_bef_, win_aft)

    # Определение веоятностных характеристик
    print("\nОпределение вероятностных характеристик")
    num_po = np.array([])
    num_lt = np.array([])
    num_pc = np.array([])
    i = 0
    for p_osh in p_osh_array:
        i += 1
        print('\rtest:' + str(i) + '/' + str(len(p_osh_array)), end='')
        num_po_, num_lt_, num_pc_ = test_probability(num_test,
                                                     surge_ps,
                                                     win_bef_,
                                                     win_aft,
                                                     porog_,
                                                     surge_ps_index,
                                                     p_osh)
        num_po = np.append(num_po, num_po_)
        num_lt = np.append(num_lt, num_lt_)
        num_pc = np.append(num_pc, num_pc_)
    po_ = num_po/num_test/n_surge
    lt_ = num_lt/num_test/n_surge
    pc_ = num_pc/num_test/n_surge
    return prob_, po_, lt_, pc_, win_, win_bef_, win_aft, porog_


def f_probability(data_, before_win_len, after_win_len):
    """ Функция вычисления отношения правдоподобия
    data_ - входной массив, тип list
    before_win_len - длина окна до скачка
    after_win_len - длина окна после скачка"""
    # Формирование массива для хранения значений отношения правдободобия скользящего окна
    probability = np.array([0] * (data_.size - before_win_len - after_win_len))
    for i in range(data_.size - before_win_len - after_win_len):
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
        try:
            probability[i] = (mean_after - mean_before) * summ / var_all
        except BaseException as err:
            print(err)
    return probability


def optimum_win_param(signal, step_win):
    """Функция определения оптимальных размеров окна, участка до скачка и участка после скачка
    signal - входной временной ряд
    step_win - шаг изменения размера окна (четное)"""
    print("\nПоиск оптимальных параметров окна по максимуму функции отношения правдоподобия.")
    max_len_win = signal.size  # Максимальный размер окна не превышает половины длины временного ряда
    len_win_cur = np.arange(step_win, max_len_win, step_win)  # Текущий размер окна
    len_win_bef = np.arange(step_win // 2, max_len_win - (step_win // 2), step_win//2)  #
    max_prob = np.zeros([len_win_cur.size, len_win_bef.size])
    numtest_win = len_win_cur.size
    numtest_win_bef = len_win_bef.size
    numtest = numtest_win * numtest_win_bef
    i = 0
    for len_win_ind in range(len_win_cur.size):
        for len_win_bef_ind in range(len_win_bef.size):
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


def full_surf_win_param(signal, step_win):
    """Функция определения оптимальных размеров окна, участка до скачка и участка после скачка
    signal - входной временной ряд
    step_win - шаг изменения размера окна (четное)"""
    print("\n\nПостроение поверхности отношения прадоподобия.")
    max_len_win = signal.size / 2  # Максимальный размер окна не превышает половины длины временного ряда
    len_win_bef = np.arange(step_win // 2, max_len_win - (step_win // 2), step_win // 2, dtype=np.int16)  #
    len_win_aft = np.arange(step_win // 2, max_len_win - (step_win // 2), step_win // 2, dtype=np.int16)  #
    max_prob = np.zeros([len_win_bef.size, len_win_aft.size])
    numtest_win_aft = len_win_aft.size
    numtest_win_bef = len_win_bef.size
    numtest = numtest_win_aft * numtest_win_bef
    i = 0
    for len_win_bef_i in range(len_win_bef.size):
        for len_win_aft_i in range(len_win_aft.size):
            try:
                max_prob[len_win_bef_i, len_win_aft_i] = \
                    max(f_probability(signal,
                                      len_win_bef[len_win_bef_i],
                                      len_win_aft[len_win_aft_i]))
            except BaseException as err:
                print(err)
            i += 1
            print('\rТест (%d : %d): %d/%d' % (numtest_win_bef, numtest_win_aft, i, numtest), end='')
    return max_prob, len_win_bef, len_win_aft


def add_nois(sig_, p):
    sig = np.copy(sig_)
    if p == 0:
        return sig
    num_rand = int(round(sig.size * p + 0.5))
    n_sample = np.random.randint(0, sig.size, num_rand)
    for i in range(n_sample.size):
        sig[n_sample[i]] = np.random.random()
    return sig


def test_probability(num_test, insignal, win_bef, win_aft, porog, indexes_skach, p):

    if indexes_skach.size:
        num_skach = 1
    else:
        return
    for l in range(1, indexes_skach.size):
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
            if k >= (prob.size - 1):
                break
            if prob[k] < porog:
                k += 1
                continue
            else:  # Подсчитываем индексы значений функциии правдоподобия, превышающих порог
                indexes_prob = np.array([])
                while prob[k] > porog:
                    if k >= (prob.size-1):
                        break
                    indexes_prob = np.append(indexes_prob, k + win_bef)
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
