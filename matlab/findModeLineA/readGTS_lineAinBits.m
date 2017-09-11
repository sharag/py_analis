
%% Преобразование ГТС А-линии в битовый вид
clc
clear

load e:\MATscripts\commuts\07.03.98\GTS_A.mat
bitmask = [128 64 32 16 8 4 2 1];
GTSinBit = false(size(GTS_Aline, 1), size(GTS_Aline, 2) * 8);
persentStep = fix(size(GTS_Aline, 1)/10000);
% Медианная фильтрация
for i = 1:size(GTS_Aline, 2)
    GTS_Aline(:,i) = medfilt1(GTS_Aline(:,i),5);
end
% Преобразование
for i = 1:size(GTS_Aline, 1)
    for j = 1:size(GTS_Aline, 2)
        for k = 1:8
            if (bitand(GTS_Aline(i,j), bitmask(k)))
                GTSinBit(i, ((j - 1) * 8 + k)) = true;
            end
        end
    end
    if rem(i,persentStep) == 0
        disp([num2str(i/100/persentStep), ' %']);
    end
end
save GTSinBits GTSinBit

%% Building histogramm of change of bits
clc
clear

load GTSinBits
histBitChange = zeros(1,size(GTSinBit, 2));
persentStep = fix(size(GTSinBit, 2)/100);
for j = 1:size(GTSinBit, 2)
    for i = 2:size(GTSinBit, 1)
        if GTSinBit(i, j) ~= GTSinBit(i - 1, j)
            histBitChange(j) = histBitChange(j) + 1;
        end
    end
    disp([num2str(j/persentStep), ' %']);
end
save histBitChange histBitChange
   
%% Processing the histogramm of change of bits
clc 
clear

load histBitChange
histBitChange1 = zeros(size(histBitChange, 1), size(histBitChange, 2));

% Нормирование гистограммы. Единица - где количество изменений разряда 0
% или 1
for i = 1:size(histBitChange, 2)
    if histBitChange(i) == 1
        histBitChange1(i) = 1;
    end
end
% Ищем только тройные цепочки в рамках одного слова
histChange = zeros(size(histBitChange, 1), size(histBitChange, 2));
for i = 1:size(histBitChange1, 2) - 2
    if (histBitChange1(i) > 0) && (histBitChange1(i + 1) > 0) && (histBitChange1(i + 2) > 0)
        disp(['position: ', num2str(i)]);
        if fix((i - 1)/8) == fix(((i - 1) + 2) / 8)
            histChange(i:i + 2) = 1;
        end
    end
end

plot(histChange);
ylim([-1 2]);
