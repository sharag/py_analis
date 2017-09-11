%% ВЕЙВЛЕТ-АНАЛИЗ
% Определение оптимального интервала ускорения для формирования вейвлета
clc
clear

%% СОЗДАНИЕ КАТАЛОГОВ
defDir = 'g:\fedorenko_ns\MATscripts\wawelets\optimumWaweletForAccel';
defDir = uigetdir(defDir, 'Выберите каталог с проектом');
% Создание каталога с результатами исследования
% и для промежуточных данных
[pathRez, pathData] = FCreateDir(defDir); 

%% ОСНОВНЫЕ ПАРАМЕТРЫ
fileTypeTMP = 'int16'; % Тип файлов
freqDiskrData = 100; % частота следования отсчетов в секунду
dScale = 0.8; %Вариация масштабов в долях

%% ОТКРЫТИЕ ФАЙЛОВ
% Открытие файла с Модулем ускорения
TMPFName = 'g:\fedorenko_ns\MATscripts\wawelets\baseTMP\T2-1d.bit.20.D1_A.tlm';
if isequal(TMPFName, 0)
    display('Ошибка.');
    display('Файл с ТМП модуля ускорения не найден.');
    return
else
    display(['Файл модуля ускорения: ' TMPFName]);
end
TMPFID = fopen(TMPFName, 'r');
TMPData = fread(TMPFID, fileTypeTMP);
fclose(TMPFID);
clear TMPFID
% Открытие файла с ТМП "Режимы"
ModeFName = 'g:\fedorenko_ns\MATscripts\wawelets\baseTMP\T2-1d.bit.14.D4.tlm';
if isequal(ModeFName, 0)
    display('Ошибка.');
    display('Файл с ТМП "Режимы" не найден.');
    return
else
    display(['Файл ТМП "Режимы": ' ModeFName]);
end
ModeFID = fopen(ModeFName, 'r');
ModeData = fread(ModeFID, fileTypeTMP);
fclose(ModeFID);
clear ModeFID
% График
figure;
TMPName = 'Модуль ускорения и каналы режимов';
Message = 'Графики модуля ускорения и ТМП "Режимы"';
TMPAxeX = (1/freqDiskrData:1/freqDiskrData:length(TMPData)/freqDiskrData)';
set(gcf, 'Name', TMPName, 'ToolBar', 'figure');
plot(TMPAxeX, TMPData, TMPAxeX, ModeData, 'LineWidth', 2);
title(Message, 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
legend('Модуль ускорения', 'ТМП "Режимы"');
save([pathRez 'WData.mat']);

%% ПОСТРОЕНИЕ ВЕЙВЛЕТА
clc
clear
load('g:\fedorenko_ns\MATscripts\wawelets\optimumWaweletForAccel\Results\WData.mat')
scale = 350;
event = 6235;

% Параметр без обработки
DataTemp = medfilt1(TMPData(1000:12300), 10);

% Параметр с нулевой энергией
meanData = mean(DataTemp);
DataTemp0 = DataTemp - meanData;

% Нормированный ТМП с нулевой энергией
diapazon = max(DataTemp0) - min(DataTemp0);
DataTempNorm = (DataTemp0 - max(DataTemp0) + diapazon/2)./(diapazon/2);
clear diapazon meanData

save([pathRez 'WData1.mat']);

clc
clear
load('g:\fedorenko_ns\MATscripts\wawelets\optimumWaweletForAccel\Results\WData1.mat')

lengthWawe = 800;
stepWawe = 10;
sum = 0;
% Определение количества итераций 
for i = 1:1:(lengthWawe/stepWawe)  %ширина вейвлета
    for j = 1:1:i+1  %смещение начала вейвлета от события
        sum=sum+1;
    end
end
numIter = sum;
sum = 0;

for i = 1:1:(lengthWawe/stepWawe)  %ширина вейвлета
    for j = 1:1:i+1  %смещение начала вейвлета от события
        ii = i*stepWawe;
        jj = j*stepWawe;
        beginPart = event-jj; % положение начала искомого интервала по-умолчанию
        endPart = beginPart+ii; % положение конца искомого интервала по-умолчанию
        % Выбор искомого интервала
        WaweData = TMPData(beginPart:1:endPart);
        % Получение вейвлета
        [psi_WData, xval_WData, nc_WData] = pat2cwav(WaweData', 'polynomial', 60, 'continuous');
        % Вейвлет-преобразование
        % Параметр без обработки
        Sc = cwt(DataTemp, scale, psi_WData);
        Mmax(i,j) = max(max(Sc));
        Mmean(i,j) = mean(mean(Sc));
        
        % Параметр с нулевой энергией
        Sc = cwt(DataTemp0, scale, psi_WData);
        Mmax0(i,j) = max(max(Sc));
        Mmean0(i,j) = mean(mean(Sc));
        
        % Нормированный ТМП
        Sc = cwt(DataTempNorm, scale, psi_WData);
        MmaxNorm(i,j) = max(max(Sc));
        MmeanNorm(i,j) = mean(mean(Sc));
        
        sum = sum + 1;
        if sum/10 == fix(sum/10)
            display(['Выполнено:' num2str(sum*100/numIter) '%']);
        end
    end
end
clear i j ii jj Sc psi_WData xval_WData nc_WData sum numIter stepWawe beginPart endPart scale

save([pathRez 'WData2.mat']);

% 
% 