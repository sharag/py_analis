clc
clear all
%Открытие файла
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
        value = int8(InData(i));
        GTS(frameCnt, wordInd) = value; %#ok<*SAGROW>
        wordInd = wordInd + 1;
    end
    if wordInd == 357
        wordInd = 1;
        syncFound = 0;
    end
    %Вывод прогресса
    if ((i/100000) == floor(i/100000))
        disp(['Текущий прогресс: ', num2str(i*100/length(InData)), '%.']);
    end
end
%Сохранение результатов
save(fullfile(InPath, [InFileName '.mat']));