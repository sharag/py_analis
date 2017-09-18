%% Описание
% Модуль исследования разладки
clc
clear

%% Характеристики исследования
len0 = 100;  % длина холостого участка
kSurge = 0.5;  % Коэффициент отношения длины временного ряда к длине скачка
skvaj = 1;  % Скважность последовательности скачков (1 - между скачками null_len)
num_s = 3;  % Количество скачков
sLen = floor(len0*kSurge);  % Длина скачка
stepWin = 10;  % Шаг изменения окна (минимум 2)
numOrder = 16;  % Количество разрядов отсчетов для учета вероятности ошибки
numTest = 10;  % Количество экспериментов для каждого значения вероятности ошибки
koefPorog = 0.9;  % Пороговое значение как коэффициент, определяющий долю от максимума отношения правдоподобия

%% Массив вероятностей ошибок в завсимости от разрядности каналов
Posh = [0.0001 : 0.0001 : 0.001, 0.001 : 0.001 : 0.01, 0.01 : 0.01 : 0.02];
Posh = Posh * numOrder;

%% Формирование скачков

[surge_ps, surge_ps_ind] = ...
    get_surge_ps(len0, sLen, skvaj, num_s);
[surge_x1, surge_x1_ind] = ...
    get_surge_x1(len0, sLen, skvaj, num_s);
[surge_x2, surge_x2_ind] = ...
    get_surge_x2(len0, sLen, skvaj, num_s);
[surge_hcos, surge_hcos_ind] = ...
    get_surge_hcos(len0, sLen, skvaj, num_s);

%% Подбор окна и построение функции отношения правдоподобия
signal = surge_ps;
% Поиск параметров окна, дающих максимум функции отношения правдоподобия
[win, winBef, winAft, maxProbVal] = getWinSize(signal, stepWin);
porog = koefPorog * maxProbVal;
% График функции отношения правдоподобия
probability = get_probability( signal, winBef, winAft );

%% Исследование вероятностных характеристик

numPO = zeros(0);
numLT = zeros(0);
numPC = zeros(0);



