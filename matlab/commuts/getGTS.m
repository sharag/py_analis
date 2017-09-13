%% Чтение сырых данных
clc;
clear;
disp('Чтение данных из файла...');
data = filereader('uint8');
data = data';
fpathMAT = uigetdir('e:\MATscripts\', 'Выберите каталог для сохранения результатов');
disp('Чтение данных завершено.');
disp('Сохранение данных...');
save([fpathMAT '\' 'data_raw.mat'], 'data', 'fpathMAT');
disp('Сохранение данных завершено.');

%% Ревес бит в байте
disp('Реверс бит...');
dataRev = reversBit(data, 8);
disp('Реверс бит завершен.');
disp('Сохранение данных...');
save([fpathMAT '\' 'data_revers.mat'], 'dataRev', 'fpathMAT');
disp('Сохранение данных завершено.');

%% Получение потока в битовом виде
disp('Преобразование в битовый вид...');
dataBit = convertToBits(dataRev, 8);
disp('Преобразование завершено.');
disp('Сохранение данных...');
save([fpathMAT '\' 'data_bits.mat'], 'dataBit', 'fpathMAT');
disp('Сохранение данных завершено.');

%% Формирование ГТС в битовом виде
disp('Синхронизация, выравнивание и формирование ГТС в битовом виде...');
lenFrame = 2880;
lenSinhr = 24;
porogHem = 3;
sinhra = '0x0db573';
dataSinhr = formBitGTS(dataBit, lenFrame, lenSinhr, sinhra, porogHem);
disp('Формирование ГТС в битовом виде завершено.');
disp('Сохранение данных...');
save([fpathMAT '\' 'data_sinhr.mat'], 'dataSinhr', 'fpathMAT');
disp('Сохранение данных завершено.');

%% Преобразование в ГТС
disp('Преобразование в слова ГТС...');
lenWord = 8;
GTS = formChanelsGTS(dataSinhr, lenWord);
disp('ГТС сформирован...');
disp('Сохранение данных...');
save([fpathMAT '\' 'GTS_A.mat'], 'GTS', 'fpathMAT');
disp('Сохранение данных завершено.');

%%
