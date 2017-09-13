clc;
clear;

freqFrame = 100; %частота следования отсчетов в секунду
stepTime = 1/freqFrame; %Шаг временной сетки с учетом децимации
clear fqFrAcclrt

[FNameData, PathFNameData] = uigetfile({'*.*', 'Файл ТМП'}, ...
    'Выберите файл ТМП', 'E:\MATscripts\findAccel\');
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
    fclose(FIDData);
    exit;
end

Data = medfilt1(Data,3);
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

figure;subplot(3,1,1);
plot(axeTime, Data, 'LineWidth', 2);
title('Ускорение 1', 'FontName', 'Times New Roman',...
    'FontSize', 10);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);





[FNameData, PathFNameData] = uigetfile({'*.*', 'Файл ТМП'}, ...
    'Выберите файл ТМП', 'E:\MATscripts\findAccel\');
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
    fclose(FIDData);
    exit;
end

Data = medfilt1(Data,3);
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

subplot(3,1,2);
plot(axeTime, Data, 'LineWidth', 2);
title('Ускорение 2', 'FontName', 'Times New Roman',...
    'FontSize', 10);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);





[FNameData, PathFNameData] = uigetfile({'*.*', 'Файл ТМП'}, ...
    'Выберите файл ТМП', 'E:\MATscripts\findAccel\');
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
    fclose(FIDData);
    exit;
end

Data = medfilt1(Data,3);
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

subplot(3,1,3);
plot(axeTime, Data, 'LineWidth', 2);
title('Ускорение 3', 'FontName', 'Times New Roman',...
    'FontSize', 10);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

