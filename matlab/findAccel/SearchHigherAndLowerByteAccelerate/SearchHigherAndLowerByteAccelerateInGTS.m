clc;
clear;
%Параметры
decimaVal = 1;%количество повторяющихся отсчетов в массиве ускорения
fqFrAcclrt = 400;%частота следования отсчетов в секунду
%Промежуточные вычисления
fqFrAcclrt = fqFrAcclrt/decimaVal;%частота следования отсчетов в секунду
stepTimeAcclrt = 1/fqFrAcclrt;%Шаг временной сетки с учетом децимации
clear fqFrAcclrt
%Чтение файлов
[InFileName, InPath] = uigetfile('*.bit','Выберите файл ГТС A-линии', ...
    'D:\work\telemetry\trident\');
if isequal(InFileName, 0)
   disp('Выбор файла отменен.')
else
   disp(['Выбран файл: ', fullfile(InPath, InFileName), '.'])
end
%Чтение файла ГТС
disp('Открытие файла.')
InFID = fopen(fullfile(InPath, InFileName), 'r');
InData = fread(InFID, 'uint8');%чтение массива данных
fclose(InFID);
clear InFID
disp('Чтение файла завершено.')
%Реверс бит в байтах
% disp('Реверс бит в байтах.')
% x = 0:1:255;
% xx = bitrevorder(x);
% for i = 1:1:length(InData)
%     InData(i) = xx(InData(i) + 1);
% end
% clear x xx
% %Запись файла с реверсом бит
% RevFID = fopen(fullfile(InPath, [InFileName '.rev.bit']), 'w');
% fwrite(RevFID, InData, 'uint8');%чтение массива данных
% fclose(RevFID);
% clear RevFID
%Заполнение ГТС
disp('Заполнение ГТС.')
syncFound = 0;
frameCnt = 0;%Индекс по кадрам
wordInd = 1;%Индекс по словам
for i = 1:1:length(InData)
    %Поиск синхры
    if (i > 3) && (InData(i - 3) == 13) && (InData(i - 2) == 181) && ...
            (InData(i - 1) == 115) && (syncFound == 0)
        syncFound = 1;
        frameCnt = frameCnt + 1;
    end
    %Заполнение массива
    if syncFound == 1
        GTS(frameCnt, wordInd) = int8(InData(i)); %#ok<*SAGROW>
        wordInd = wordInd + 1;
    end
    if wordInd == 358
        wordInd = 1;
        syncFound = 0;
    end
    %Вывод прогресса
    if ((i/10000) == floor(i/10000))
        disp(['Текущий прогресс: ', num2str(i*100/length(InData)), '%.']);
    end
end
clear wordInd frameCnt syncFound
%Сохранение результатов
save(fullfile(InPath, [InFileName '.mat']));

%//////////////////////////////////////////////////////////////////////////

%Загрузка рабочих переменных
%Открытие файла рабочей области
[wrkSpcFileName, wrkSpcPath] = uigetfile('*.mat','Выберите файл рабочей области (workspace)', ...
    'D:\work\telemetry\trident\');
if isequal(wrkSpcFileName, 0)
   disp('Выбор файла workspace отменен.')
else
   disp(['Выбран файл workspace: ', fullfile(wrkSpcPath, wrkSpcFileName), '.'])
end
load(fullfile(wrkSpcPath, wrkSpcFileName));
disp('Файл рабочей облати загружен.')


sostNum = 3;
% Статистика
transitStat = zeros(sostNum, sostNum, 2);
for i = 1:1:sostNum
    for j = 1:1:size(DataAcclrt, 2)
        if (j >= 2) && (accelPartsHight(i, j) ~= accelPartsHight(i, j-1));
            for k = 1:1:sostNum
                transitStat(i, k, 1) = transitStat(i, k, 1) + 1;
                if (abs(accelPartsLow(k, j) - accelPartsLow(k, j-1)) > 224)
                    transitStat(i, k, 2) = transitStat(i, k, 2) + 1;
                end
            end
        end
    end
end
razn = transitStat(:, :, 1) - transitStat(:, :, 2);
x = transitStat(:,:,1);
xx = transitStat(:,:,2);

%Ось времени для ускорения
axeTimeAcclrt = (0:stepTimeAcclrt:...
    (size(DataAcclrt, 2)*stepTimeAcclrt)-stepTimeAcclrt)';
clear stepTimeAcclrt

hightDigit = accelPartsHight(1, :).*256;
incor1 = hightDigit + accelPartsLow(3, :);
incor2 = hightDigit + accelPartsLow(1, :);

figure(1);
plot(axeTimeAcclrt, DataAcclrt(1, :), axeTimeAcclrt, hightDigit,...
    axeTimeAcclrt, incor1, axeTimeAcclrt, incor2, 'LineWidth', 2);
title('Определение соответствия младших слов старшему', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('Исходное ускорение', 'Старшее слово', 'Неверное младшее слово 1', 'Неверное младшее слово 2');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);


counter = zeros(1, size(DataAcclrt, 2));
dir = 1;
j = 1;
for i=1:1:size(DataAcclrt, 2)
    if (dir == 1) && ((i/40) == floor(i/40))
        j = j + 1;
    elseif (i/40) == floor(i/40)
        j = j - 1;
    end
    counter(i) = j;
    if j == 2^16
        dir = 0;
    elseif j == 0
        dir = 1;
    end
end

counterLow = mod(counter, 256);
hightAndLowCounter = hightDigit + counterLow;
figure(2);
plot(axeTimeAcclrt, DataAcclrt(1, :), axeTimeAcclrt, counter,...
    axeTimeAcclrt, hightAndLowCounter, 'LineWidth', 2);
title('Определение соответствия младших слов старшему', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('Время полета, с', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('Значение', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('Исходное ускорение', 'Счетчик на 16 разрядов', 'Старшее слово и мл.р.счетчика');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);