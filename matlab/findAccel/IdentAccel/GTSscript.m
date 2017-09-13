clc
clear all
%Открытие файла
[InFileName, InPath] = uigetfile('*.bit','Выберите файл ГТС A-линии', ...
    'D:\work\telemetry\trident\');
if isequal(InFileName, 0)
   disp('Выбор файла отменен.')
   break
else
   disp(['Выбран файл: ', fullfile(InPath, InFileName), '.'])
end
%Чтение файла ГТС
disp('Открытие файла.')
InFID = fopen(fullfile(InPath, InFileName), 'r');
InData = fread(InFID, 'int8');%чтение массива данных
fclose(InFID);
clear InFID
% %Реверс бит в байтах
% disp('Реверс бит в байтах.')
% x = 0:1:255;
% xx = bitrevorder(x);
% for i = 1:1:length(InData)
%     InData(i) = xx(InData(i) + 1);
% end
% clear x xx
% %Запись файла с реверсом бит
% RevFID = fopen(fullfile(InPath, [InFileName '.rev.bit']), 'w');
% fwrite(RevFID, InData, 'uint8');%запись массива данных
% fclose(RevFID);
% clear RevFID
%Заполнение ГТС
disp('Заполнение ГТС.')
syncFound = 0;
frameCnt = 0;%Индекс по кадрам
forDisp = 0.01;
for i = 4:1:size(InData, 1)
    %Поиск синхры
    if (abs(InData(i - 3) - 13) <= 2) && (abs(InData(i - 2) + 75) <= 2) && ...
            (abs(InData(i - 1) - 115) <= 2) && (syncFound == 0)
        syncFound = 1;
        frameCnt = frameCnt + 1;
    end
    %Заполнение массива
    if syncFound == 1
        GTS(frameCnt, : ) = InData((i - 3):1:(i + 356));
        syncFound = 0;
        i = i + 353; %#ok<FXSET>
    end
    %Вывод прогресса
    if ((i*100/size(InData, 1)) > forDisp)
        disp(['Текущий прогресс: ', num2str(i*100/size(InData, 1)), '%.']);
        forDisp = forDisp + 0.01;
        disp(['Кадр ' num2str(frameCnt)]);
    end
end
clear frameCnt syncFound wordInd
%Сохранение результатов
save(fullfile(InPath, [InFileName '.mat']));
% Поиск составляющих ускорения
disp('Поиск составляющих ускорения.');
value = 0;
valCount = 0;
countPeriod = 0;
numAccelParts = 0;
for i = 1:1:size(GTS, 2)
    for j = 1:1:8000
        if GTS(j, i) == value && valCount <= 40
            valCount = valCount + 1;
        elseif (40 - valCount) <= 1
            valCount = 0;
            value = GTS(j, i);
            countPeriod = countPeriod + 1;
        else
            valCount = 0;
            value = GTS(j, i);
        end
    end
    if countPeriod > 200
        disp(['Слово : ', num2str(i + 3), '.']);
        countPeriod = 0;
        numAccelParts = numAccelParts + 1;
        accelParts(numAccelParts, : ) = GTS(:, i );
        numbersOfParts(numAccelParts) = i;
    end
end
