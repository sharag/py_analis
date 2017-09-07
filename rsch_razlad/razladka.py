"""
Модуль исследования разладки
"""

from rsch_razlad.functions import *
import pickle

# Характеристики исследования
null_len = 100  # длина холостого участка
k_surge = 0.5  # Коэффициент отношения длины временного ряда к длине скачка
skvaj = 1  # Скважность последовательности скачков (1 - между скачками null_len)
n_surge = 3  # Количество скачков
surge_len = int(null_len*k_surge)  # Длина скачка
step_win = 10  # Шаг изменения окна (минимум 2)
num_order = 16  # Количество разрядов отсчетов для учета вероятности ошибки
num_test = 10  # Количество экспериментов для каждого значения вероятности ошибки
koef_porog_ = 0.9  # Пороговое значение как коэффициент, определяющий долю от максимума отношения правдоподобия

# Путь к файлу со скачками
path = 'e:\\git\\data\\razlad\\surge'

# Массив вероятностей ошибок
p_osh_array = np.linspace(0.0001, 0.001, 10)
p_osh_array = np.append(p_osh_array, np.linspace(0.001, 0.01, 10))
p_osh_array = np.append(p_osh_array, np.linspace(0.01, 0.02, 2))
p_osh_array = p_osh_array*num_order

surges = []
print('\n\nИсследование кратковременного скачка постоянной составляющей')
surge, surge_ps_index = get_post_sost(null_len, surge_len, skvaj, n_surge)
# Исследование скачка
prob, po, lt, pc, win, win_bef, win_aft, porog = research_surge(surge,
                                                                surge_ps_index,
                                                                step_win,
                                                                koef_porog_,
                                                                num_test,
                                                                p_osh_array,
                                                                n_surge)
max_prob_surf, len_win_x, len_win_bef_y = full_surf_win_param(surge, step_win)

surges.append({'name': 'Прямоугольный импульс',
               'surge': surge,
               'prob': prob,
               'PO': po,
               'LT': lt,
               'PC': pc,
               'p_osh_array': p_osh_array,
               'surf': {'surf': max_prob_surf,
                        'x': len_win_x,
                        'y': len_win_bef_y},
               'opt': {'win': win,
                       'win_bef': win_bef,
                       'win_aft': win_aft,
                       'porog': porog}})


print('\n\nИсследование кратковременного скачка c линейным изменением значений')
surge, surge_ps_index = get_lin(null_len, surge_len, skvaj, n_surge)
# Исследование скачка
prob, po, lt, pc, win, win_bef, win_aft, porog = research_surge(surge,
                                                                surge_ps_index,
                                                                step_win,
                                                                koef_porog_,
                                                                num_test,
                                                                p_osh_array,
                                                                n_surge)

surges.append({'name': 'Импульс с линейным изменением значений',
               'surge': surge,
               'prob': prob,
               'PO': po,
               'LT': lt,
               'PC': pc,
               'p_osh_array': p_osh_array,
               'opt': {'win': win,
                       'win_bef': win_bef,
                       'win_aft': win_aft,
                       'porog': porog}})


print('\n\nИсследование кратковременного скачка c квадратическим изменением значений')
surge, surge_ps_index = get_kvadr(null_len, surge_len, skvaj, n_surge)
# Исследование скачка
prob, po, lt, pc, win, win_bef, win_aft, porog = research_surge(surge,
                                                                          surge_ps_index,
                                                                          step_win,
                                                                          koef_porog_,
                                                                          num_test,
                                                                          p_osh_array,
                                                                          n_surge)

surges.append({'name': 'Импульс с квадратическим изменением значений',
               'surge': surge,
               'prob': prob,
               'PO': po,
               'LT': lt,
               'PC': pc,
               'p_osh_array': p_osh_array,
               'opt': {'win': win,
                       'win_bef': win_bef,
                       'win_aft': win_aft,
                       'porog': porog}})


print('\n\nИсследование кратковременного скачка типа приподнятого косинуса')
surge, surge_ps_index = get_high_cos(null_len, surge_len, skvaj, n_surge)
# Исследование скачка
prob, po, lt, pc, win, win_bef, win_aft, porog = research_surge(surge,
                                                                surge_ps_index,
                                                                step_win,
                                                                koef_porog_,
                                                                num_test,
                                                                p_osh_array,
                                                                n_surge)

surges.append({'name': 'Импульс типа приподнятого косинуса',
               'surge': surge,
               'prob': prob,
               'PO': po,
               'LT': lt,
               'PC': pc,
               'p_osh_array': p_osh_array,
               'opt': {'win': win,
                       'win_bef': win_bef,
                       'win_aft': win_aft,
                       'porog': porog}})


with open(path, 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(surges, f, pickle.HIGHEST_PROTOCOL)
