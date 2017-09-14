%% Описание
% Модуль исследования разладки

%% Характеристики исследования
null_len = 100;  % длина холостого участка
k_surge = 0.5;  % Коэффициент отношения длины временного ряда к длине скачка
skvaj = 1;  % Скважность последовательности скачков (1 - между скачками null_len)
n_surge = 3;  % Количество скачков
surge_len = floor(null_len*k_surge);  % Длина скачка
step_win = 10;  % Шаг изменения окна (минимум 2)
num_order = 16;  % Количество разрядов отсчетов для учета вероятности ошибки
num_test = 10;  % Количество экспериментов для каждого значения вероятности ошибки
koef_porog_ = 0.9;  % Пороговое значение как коэффициент, определяющий долю от максимума отношения правдоподобия

%% Формирование скачков

[surge_ps, surge_ps_ind] = get_surge_ps(null_len, surge_len, skvaj, n_surge);
[surge_x1, surge_x1_ind] = get_surge_x1(null_len, surge_len, skvaj, n_surge);
[surge_x2, surge_x2_ind] = get_surge_x2(null_len, surge_len, skvaj, n_surge);
%surge_ps, surge_lin, surge_kvadr, surge_highcos = get_surge_ps(null_len, surge_len, skvaj, n_surge);

