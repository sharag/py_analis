"""
Модуль формирования скачков
"""
import numpy as np
import copy


def get_post_sost(null_len, surge_len, skvaj, n_surge):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками
    n_surge - количество скачков"""
    # 0
    surge_ps = [0] * null_len
    surge_ps_indexes = []
    n = n_surge

    while n:
        n -= 1
        # 1
        surge_ps_indexes.extend([i for i in range(len(surge_ps), len(surge_ps) + surge_len)])
        surge_ps.extend([1] * surge_len)
        # 0
        surge_ps.extend([0] * int(null_len * skvaj))

    return surge_ps, surge_ps_indexes


def research_surge(surge_ps, surge_ps_index, step_win, koef_porog_, num_test, p_osh_array, n_surge):
    """Исследование скачка постоянной составляющей"""
    # Скачок постоянной составляющей
    #surge_ps, surge_ps_index = get_post_sost(null_len, surge_len, 1)

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
    print("\n\nОпределение вероятностных характеристик")
    num_po = list()
    num_lt = list()
    num_pc = list()
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
        num_po.append(num_po_)
        num_lt.append(num_lt_)
        num_pc.append(num_pc_)
    po_ = np.array(num_po)/num_test/n_surge
    lt_ = np.array(num_lt)/num_test/n_surge
    pc_ = np.array(num_pc)/num_test/n_surge
    return surge_ps, prob_, po_, lt_, pc_, win_, win_bef_, win_aft, porog_


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
