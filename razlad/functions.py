"""
Модуль формирования скачков
"""
import numpy as np
import copy


class FormSurge:
    """ Класс для формирования скачков """

    def __init__(self):
        """ Инициализация класса """
        self.cur_surge = 0
        self.num_surge = 7

    def get_surge(self, n_surge, win_len):
        """Функция, возвращающая при каждом вызове очередной скачок
        Принимаемый аргумент: win_len - задаваемая щирина окна
        Возвращаемые значения:
            массив - для графика
            название
            список моментов начала очередного скачка
            список характеристик скачков"""
        if n_surge is not None:
            self.cur_surge = n_surge
        if self.cur_surge == 0:
            """Первый скачок - скачок постоянной составляющей.
            Без входных аргументов. На выходе список на 1000 элементов."""
            surge = [0] * (win_len + 100 - (win_len + 100) % 100)
            surge.extend([1] * (win_len + 100 - (win_len + 100) % 100))
            self.cur_surge += 1
            return surge, 'Скачок постоянной составляющей', None, None
        elif self.cur_surge == 1:
            surge = [0] * (win_len + 100 - (win_len + 100) % 100)
            surge_list = []
            surge_prop = []
            for i in range(10, win_len + win_len//2, win_len//10):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([1] * i)
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            self.cur_surge += 1
            return surge, 'Кратковременные скачки постоянной составляющей', surge_list, surge_prop
        elif self.cur_surge == 2:
            surge = [0] * (win_len + 100 - (win_len + 100) % 100)
            surge_list = []
            surge_prop = []
            for i in range(10, win_len + win_len // 2, win_len // 10):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([x / i for x in range(i)])
                surge.extend([1] * (win_len + 100 - (len(surge) + win_len) % 100))
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([1 - x / i for x in range(i)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            for i in range(win_len + win_len // 2, win_len * 10, win_len // 2):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([x / i for x in range(i)])
                surge.extend([1] * (win_len + 100 - (len(surge) + win_len) % 100))
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([1 - x / i for x in range(i)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            self.cur_surge += 1
            return surge, 'Линейные изменения постоянной составляющей', surge_list, surge_prop
        elif self.cur_surge == 3:
            surge = [0] * (win_len + 100 - (win_len + 100) % 100)
            surge_list = []
            surge_prop = []
            for i in range(10, win_len + win_len // 2, win_len // 10):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([x / i for x in range(i)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            for i in range(win_len + win_len // 2, win_len * 10, win_len // 2):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([x / i for x in range(i)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            self.cur_surge += 1
            return surge, 'Линейное изменение постоянной составляющей и сброс', surge_list, surge_prop
        elif self.cur_surge == 4:
            max_point = 1000
            min_point = 5
            step = 10
            surge_list = []
            surge_prop = []
            surge_list.append(0)
            surge_prop.append(min_point)
            surge = [np.sin(x) for x in np.linspace(-np.pi, np.pi, min_point)[0:-1]]
            for i in range(min_point, 100, 1):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([np.sin(x) for x in np.linspace(-np.pi, np.pi, i)[0:-1]])
            for i in range(100, max_point, step):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([np.sin(x) for x in np.linspace(-np.pi, np.pi, i)[0:-1]])
            self.cur_surge += 1
            return surge, 'Гармонические колебания с изменяемой частотой', surge_list, surge_prop
        elif self.cur_surge == 5:
            surge = [0] * (win_len + 100 - (win_len + 100) % 100)
            surge_list = []
            surge_prop = []
            for i in range(10, win_len + win_len // 2, 10):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([((x * 2 / i) ** 2) / 2 for x in range(i // 2)])
                surge.extend([(1 - ((x - i / 2) / (i // 2)) ** 2) / 2 + 0.5 for x in range(i // 2)])
                surge.extend([1] * (win_len + 100 - (len(surge) + win_len) % 100))
                surge.extend([1 - (((x * 2 / i) ** 2) / 2) for x in range(i // 2)])
                surge.extend([1 - ((1 - ((x - i / 2) / (i // 2)) ** 2) / 2 + 0.5) for x in range(i // 2)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            for i in range(win_len + win_len // 2, 2000, win_len // 2):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([((x * 2 / i) ** 2) / 2 for x in range(i // 2)])
                surge.extend([(1 - ((x - i / 2) / (i // 2)) ** 2) / 2 + 0.5 for x in range(i // 2)])
                surge.extend([1] * (win_len + 100 - (len(surge) + win_len) % 100))
                surge.extend([1 - (((x * 2 / i) ** 2) / 2) for x in range(i // 2)])
                surge.extend([1 - ((1 - ((x - i / 2) / (i // 2)) ** 2) / 2 + 0.5) for x in range(i // 2)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            self.cur_surge += 1
            return surge, 'Нелинейное изменение постоянной составляющей 2 порядка', surge_list, surge_prop
        elif self.cur_surge == 6:
            surge = [0] * (win_len + 100 - (win_len + 100) % 100)
            surge_list = []
            surge_prop = []
            for i in range(10, win_len + win_len // 2, 10):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([((x * 2 / i) ** 2) / 2 for x in range(i // 2)])
                surge.extend([(1 - ((x - i / 2) / (i // 2)) ** 2) / 2 + 0.5 for x in range(i // 2)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            for i in range(win_len + win_len // 2, 2000, win_len // 2):
                surge_list.append(len(surge))
                surge_prop.append(i)
                surge.extend([((x * 2 / i) ** 2) / 2 for x in range(i // 2)])
                surge.extend([(1 - ((x - i / 2) / (i // 2)) ** 2) / 2 + 0.5 for x in range(i // 2)])
                surge.extend([0] * (win_len + 100 - (len(surge) + win_len) % 100))
            self.cur_surge += 1
            return surge, 'Нелинейное изменение постоянной составляющей 2 порядка и сброс', surge_list, surge_prop
        else:
            return None, None


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


def max_probabil(signal, win_size, surge_len, step_win):
    len_win_x = np.arange(step_win, win_size, step_win)
    len_win_bef = np.arange(int(step_win/2), win_size - int(step_win/2), int(step_win/2))
    max_prob = np.zeros([len(len_win_x), len(len_win_bef)])
    # bef_aft = np.zeros([])
    # bef_surge = np.zeros([])
    # aft_surge = np.zeros([])
    for len_win_ind in range(len(len_win_x)):
        for len_win_bef_ind in range(len(len_win_bef)):
            if len_win_x[len_win_ind] - len_win_bef[len_win_bef_ind] < 2:
                continue
            if len_win_bef[len_win_bef_ind] < len_win_x[len_win_ind] // 2:
                continue
            len_win_aft = len_win_x[len_win_ind] - len_win_bef[len_win_bef_ind]
            # bef_aft = np.append(bef_aft, len_win_bef[len_win_bef_ind] / len_win_aft)
            # bef_surge = np.append(bef_surge, [len_win_bef[len_win_bef_ind] / surge_len])
            # aft_surge = np.append(aft_surge, [len_win_aft / surge_len])
            max_prob[len_win_ind][len_win_bef_ind] = \
                max(f_probability(signal, len_win_bef[len_win_bef_ind], len_win_aft))
    return len_win_x, len_win_bef, max_prob


def add_nois(sig_, p):
    sig = copy.copy(sig_)
    if p == 0:
        return sig
    num_rand = int(round(len(sig)*p + 0.5))
    n_sample = np.random.randint(0, len(sig), num_rand)
    for i in range(len(n_sample)):
        sig[n_sample[i]] = np.random.random()
    return sig


def test_probability_list(num_test, insignal, win_bef, win_aft, porog, indexes_skach, p):
    if len(indexes_skach):
        num_skach = 1
    else:
        return
    for l in range(1, len(indexes_skach)):
        if indexes_skach[l] - indexes_skach[l-1] > 1:
            num_skach += 1
    num_po = list()  # Правильное обнаружение
    num_lt = list()  # Ложная тревога
    num_pc = list()  # Пропуск цели
    for i in range(num_test):  # Испытания
        signal = add_nois(insignal, p)
        prob = f_probability(signal, win_bef, win_aft)
        k = 0
        num_po.append(0)
        num_lt.append(0)
        num_pc.append(0)
        while True:  # Проверяем превышение порога функцией правдоподобия
            if k >= len(prob):
                break
            if prob[k] < porog:
                k += 1
                continue
            else:  # Подсчитываем индексы значений функциии правдоподобия, превышающих порог
                indexes_prob = list()
                while prob[k] > porog:
                    if k >= len(prob):
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
                    num_po[-1] += 1
                else:
                    num_lt[-1] += 1
        if num_po[-1] < num_skach:
            num_pc[-1] = num_skach - num_po[-1]
        if num_po[-1] > num_skach:
            num_lt[-1] += num_po[-1] - num_skach
    return num_po, num_lt, num_pc


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

if __name__ == '__main__':
    """Функция служит для тестирования модуля"""
    cl = FormSurge()
    surge_ = cl.get_surge()
