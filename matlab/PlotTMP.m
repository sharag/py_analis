clc;
clear;

%Параметры
freqFrame = 100;%частота следования отсчетов в секунду

%Промежуточные вычисления
stepTime = 1/freqFrame;%Шаг временной сетки с учетом децимации
clear fqFrAcclrt

%Чтение файлов
[FNameData, PathFNameData] = uigetfile({'*.*', 'Файл ТМП'}, ...
    'Выберите файл ТМП', 'C:\Users\fedorenko\Desktop\для практики\TMSignals');
if isequal(FNameData, 0)
   disp('Выбор файла отменен.');
   exit
else
   disp(['Выбран файл: ', fullfile(PathFNameData, FNameData), '.']);
end

FIDData = fopen(fullfile(PathFNameData, FNameData), 'r');
Data = fread(FIDData, 'int16');
if (length(Data) < 3)
    disp('Слишком маленький файл.');
end
fclose(FIDData);

%Ось времени для ускорения
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

%Построение графиков компонент ускорения и модуля ускорения до фильтрации
figure;
plot(axeTime, Data./10, 'LineWidth', 2);
title('Модуль ускорения', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);