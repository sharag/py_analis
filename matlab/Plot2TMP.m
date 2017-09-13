clc;
clear;
%Параметры
freqFrame1 = 100;%частота следования отсчетов в секунду
freqFrame2 = 100;%частота следования отсчетов в секунду
%Промежуточные вычисления
stepTime1 = 1/freqFrame1;%Шаг временной сетки с учетом децимации
stepTime2 = 1/freqFrame2;%Шаг временной сетки с учетом децимации
%Коэффициенты для параметров
koef1 = 1;%1;
koef2 = 1;%1/20;
%Чтение первого файла
[FNameData1, PathFNameData1] = uigetfile({'*.*', 'Файл ТМП'}, ...
    'Выберите первый файл с ТМП', ...
    'C:\Users\fedorenko\Desktop\для практики\TMSignals');
if isequal(FNameData1, 0)
   disp('Выбор файла отменен.');
   exit
else
   disp(['Выбран файл: ', fullfile(PathFNameData1, FNameData1), '.']);
end
FIDData1 = fopen(fullfile(PathFNameData1, FNameData1), 'r');
Data1 = fread(FIDData1, 'int16');%'float');
if (length(Data1) < 3)
    disp('Слишком маленький файл.');
end
fclose(FIDData1);
%Чтение второго файла
[FNameData2, PathFNameData2] = uigetfile({'*.*', 'Файл ТМП'}, ...
    'Выберите второй файл с ТМП', ...
    'C:\Users\fedorenko\Desktop\для практики\TMSignals');
if isequal(FNameData2, 0)
   disp('Выбор файла отменен.');
   exit
else
   disp(['Выбран файл: ', fullfile(PathFNameData2, FNameData2), '.']);
end
FIDData2 = fopen(fullfile(PathFNameData2, FNameData2), 'r');
Data2 = fread(FIDData2, 'uint16');
if (length(Data2) < 3)
    disp('Слишком маленький файл.');
end
fclose(FIDData2);
%Ось времени для первого параметра
axeTime1 = (0:stepTime1:(length(Data1)*stepTime1)-stepTime1)';
%Ось времени для второго параметра
axeTime2 = (0:stepTime2:(length(Data2)*stepTime2) - stepTime2)';

Data1 = Data1.*koef1;
Data2 = Data2.*koef2;

%Построение графиков компонент ускорения и модуля ускорения до фильтрации
figure;
plot(axeTime1, Data1, 'LineWidth', 2);
hold on;
plot(axeTime2, Data2, 'LineWidth', 2);
% for i = 2:length(axeTime2)
%     if Data2(i) ~= Data2(i - 1)
%         plot([axeTime2(i),axeTime2(i)],[0,5*10^4], 'b--', 'LineWidth', 2);
%     end
% end
title('Модуль ускорения и режимы', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);