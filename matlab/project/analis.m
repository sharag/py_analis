%% ВЕЙВЛЕТ-АНАЛИЗ
% ОПРЕДЕЛЕНИЕ ОСНОВНЫХ ХАРАКТЕРИСТИК ТМП
% ПОСТРОЕНИЕ ВЕЙВЛЕТА
clc
clear

%% СОЗДАНИЕ КАТАЛОГОВ
defDir = 'g:\fedorenko_ns\MATscripts\wawelets';
defDir = uigetdir(defDir, 'Выберите каталог с проектом');
% Создание каталога с результатами исследования
% и для промежуточных данных
[pathRez, pathData] = FCreateDir(defDir); 

%% ОСНОВНЫЕ ПАРАМЕТРЫ
fileTypeTMP = 'int16'; % Тип файлов
freqDiskrData = 100; % частота следования отсчетов в секунду
dScale = 0.15; %Вариация масштабов в долях

%% ПОСТРОЕНИЕ ВЕЙВЛЕТА
beginPart = 5900; % положение начала искомого интервала по-умолчанию
endPart = 6250; % положение конца искомого интервала по-умолчанию
% Открытие файла с базовым ТМП
[fullBaseTMPFName, baseTMPFName, baseTMPData] = FOpenBaseTMP(fileTypeTMP, defDir);
% Построение графика базового ТМП и выбор необходимого фрагмента
FGrafBaseTMP(baseTMPData, baseTMPFName);
% Ввод номеров значений начала и конца искомого интервала
[beginPart, endPart] = FScopePart(beginPart, endPart);
centrOfPart = floor(beginPart + (endPart - beginPart)/2);
% Выбор искомого интервала
WaweData = baseTMPData(beginPart:1:endPart);
WaweData = WaweData - mean(WaweData);
% Получение вейвлета
%[psi_WData, xval_WData, nc_WData] = pat2cwav(WaweData, 'orthcost', 3, 'continuous');%'polynomial', 10, 'continuous');
[psi_WData, xval_WData, nc_WData] = pat2cwav(WaweData', 'polynomial', 60, 'continuous');
% Построение графика построенного вейвлета
FGrafBuildW(WaweData, psi_WData, freqDiskrData);
% Сохранение результатов построения вейвлета
save([pathRez 'WData.mat']);
save([pathRez 'Data.mat'], 'baseTMPData');
%% Вейвлет-анализ набора функциональных ТМП
% Загрузка переменных
if ~exist('defDir', 'var')
    defDir = uigetdir('g:\fedorenko_ns\MATscripts\wawelets', 'Выберите каталог с проектом');
end
load([defDir '\Results\WData.mat']);
% Формирование шкалы масштаба
scale = length(psi_WData) - dScale*length(psi_WData):1:length(psi_WData) + dScale*length(psi_WData);
% Открытие каталога с анализируемыми ТМП
[files, pathTMP] = FOpenDirFunc(defDir);


for nfile = 1:1:length(files)
    % Чтение информации о файле ТМП
    infoFID = fopen([pathTMP, files(nfile).name '.txt'], 'r');
    fileType = fscanf(infoFID, '%s'); 
    fclose(infoFID);
    % Чтение файла ТМП
    infileID = fopen([pathTMP, files(nfile).name], 'r');
    DataNois = fread(infileID, fileType);
    fclose(infileID);
    % Выбор исследуемого интервала
%     Data = DataNois((beginPart - 2*freqDiskrData):(endPart + 2*freqDiskrData));
    Data = DataNois(16880:length(DataNois));%Анализ на всем ТМП
    % Устранение ошибок
    Data = medfilt1(Data, 30);
    DataTemp = Data(5:length(Data) - 5);
%     DataTemp = Data;
    clear Data
    % Оценивание на наличие перескоков
%     shift = 0;
%     for i = 2:1:length(DataTemp)
%         if DataTemp(i - 1) - DataTemp(i) > (2^15 + 2^14 + 2^13)
%             shift = shift + 2^16;
%         elseif DataTemp(i) - DataTemp(i - 1) > (2^15 + 2^14 + 2^13)
%             shift = shift - 2^16;
%         end
%         Data(i) = DataTemp(i) + shift;
%     end
    Data = DataTemp; %Если перескоки не нужны
    clear DataTemp
    % Формирование равновзвешенного интервала
    meanData = mean(Data);
    Data = Data - meanData;
    % Расширение исследуемого интервала нулями
%     DataTemp = zeros(1, 4001 + length(Data));
%     DataTemp(2001:2001 + length(Data) - 1) = Data(:);
    
    % Нормирование интервала
    maxData = abs(max(DataTemp));
    minData = abs(min(DataTemp));
    if maxData > minData
        Data = DataTemp./maxData;
    else
        Data = DataTemp./minData;
    end
    clear DataTemp
    %
    plot(Data)
    % Вейвлет-преобразование сигнала
    Sc = cwt(Data, scale, psi_WData);
    
    ScMax(nfile) = max(max(Sc));
    ScMin(nfile) = min(min(Sc));
    ScMean(nfile) = mean(mean(Sc));

    disp([num2str(nfile*100/length(files)) ' %']);
end
