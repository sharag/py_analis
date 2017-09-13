clc;
clear;

freqFrame = 400; %частота следования отсчетов в секунду
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
proizv = zeros(1,length(Data)-1);
for i=2:length(Data)
    proizv(i-1) = Data(i) - Data(i-1);
end
axeTimeProizv = axeTime;
axeTimeProizv(length(axeTimeProizv)) = [];

figure;
plot(axeTime, Data, axeTimeProizv, (proizv+1000), 'LineWidth', 2);
title('Ускорение и производная', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);

skoProizv = zeros(1,length(proizv)-freqFrame);
MOProizv = zeros(1,length(proizv)-freqFrame);
for i=1:length(skoProizv)
    skoProizv(i) = std(proizv(i:i+freqFrame));
    MOProizv(i) = mean(proizv(i:i+freqFrame));
end

figure
plot(stepTime:stepTime:length(skoProizv)*stepTime,skoProizv,...
    stepTime:stepTime:length(skoProizv)*stepTime, MOProizv, 'LineWidth', 2);
title('СКО и МО производной', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
