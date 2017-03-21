"""
Модуль формирования скачков
"""
import numpy as np


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

if __name__ == '__main__':
    """Функция служит для тестирования модуля"""
    cl = FormSurge()
    surge_ = cl.get_surge()
