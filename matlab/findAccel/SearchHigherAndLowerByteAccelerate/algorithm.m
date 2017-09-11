clc;
clear;

%���������
decVal = 40;%��������� (1/40)
fqFrAcclrt = 400;%������� ���������� �������� � �������
sostNum = 3;%���������� ������������ ���������

%������ ������
[FNameDataA0, PathFNameDataA0] = uigetfile({'*.Ai0', ...
    '���� ������������ ��������� A0'}, ...
    '�������� ���� ������������ ��������� A0',...
    'd:\work\telemetry\trident\');
if isequal(FNameDataA0, 0)
   disp('����� ����� �������.');
   break;
else
   disp(['������ ����: ', fullfile(PathFNameDataA0, FNameDataA0), '.']);
end
FIDDataA0 = fopen(fullfile(PathFNameDataA0, FNameDataA0), 'r');
DataAcclrt(1, :) = fread(FIDDataA0, 'int16');
[FNameDataA1, PathFNameDataA1] = uigetfile({'*.Ai1', ...
    '���� ������������ ��������� A1'}, ...
    '�������� ���� ������������ ��������� A1',...
    'd:\work\telemetry\trident\');
if isequal(FNameDataA1, 0)
   disp('����� ����� �������.');
   break;
else
   disp(['������ ����: ', fullfile(PathFNameDataA1, FNameDataA1), '.']);
end
FIDDataA1 = fopen(fullfile(PathFNameDataA1, FNameDataA1), 'r');
DataAcclrt(2, :) = fread(FIDDataA1, 'int16');
[FNameDataA2, PathFNameDataA2] = uigetfile({'*.Ai2', ...
    '���� ������������ ��������� A2'}, ...
    '�������� ���� ������������ ��������� A2',...
    'd:\work\telemetry\trident\');
if isequal(FNameDataA2, 0)
   disp('����� ����� �������.');
   break;
else
   disp(['������ ����: ', fullfile(PathFNameDataA2, FNameDataA2), '.']);
end
FIDDataA2 = fopen(fullfile(PathFNameDataA2, FNameDataA2), 'r');
DataAcclrt(3, :) = fread(FIDDataA2, 'int16');
clear FIDDataA0 FIDDataA1 FIDDataA2 FNameDataA0 FNameDataA1 FNameDataA2
clear PathFNameDataA1 PathFNameDataA2

%������������ ������������ ��������� - 1/40, ��� ��� ������ ���� 40 ���������� ��������
DataAcclrtDec = zeros(sostNum, floor(size(DataAcclrt, 2)/decVal));
ii = 1;
for i=1:decVal:(length(DataAcclrt) - decVal + 1)
    DataAcclrtDec(:, ii) = DataAcclrt(:, i); %#ok<SAGROW>
    ii = ii + 1;
end
fqFrAcclrt = fqFrAcclrt/decVal;%������� ���������� �������� � �������
stepTimeAcclrt = 1/fqFrAcclrt;%��� ��������� ����� � ������ ���������
clear fqFrAcclrt
disp('��������� ������������ ��������� �����������.');
clear i ii decVal

%������������ ������ ���������
accelPartsLow = zeros(sostNum, size(DataAcclrtDec, 2));
accelPartsHight = zeros(sostNum, size(DataAcclrtDec, 2));
accelPartsHight(1, :) = fix(DataAcclrtDec(1, :)./256);
accelPartsHight(2, :) = fix(DataAcclrtDec(2, :)./256);
accelPartsHight(3, :) = fix(DataAcclrtDec(3, :)./256);
accelPartsLow(2, :) = mod(DataAcclrtDec(1, :), 256);
accelPartsLow(3, :) = mod(DataAcclrtDec(2, :), 256);
accelPartsLow(1, :) = mod(DataAcclrtDec(3, :), 256);
disp('������������ ��������� ��������� �� �����.');
save([PathFNameDataA0 '..\accelParts.mat']);
clear PathFNameDataA0

% ����������
transitStat = zeros(sostNum, sostNum, 2);
for i = 1:1:sostNum
    for j = 1:1:size(DataAcclrtDec, 2)
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

%��� ������� ��� ���������
axeTimeAcclrt = (0:stepTimeAcclrt:...
    (size(DataAcclrtDec, 2)*stepTimeAcclrt)-stepTimeAcclrt)';
clear stepTimeAcclrt

hightDigit = accelPartsHight(1, :).*256;
incor1 = hightDigit + accelPartsLow(3, :);
incor2 = hightDigit + accelPartsLow(1, :);




counter = zeros(1, size(DataAcclrtDec, 2));
dir = 1;
j = 1;
for i=1:1:size(DataAcclrtDec, 2)
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

figure(1);
plot(axeTimeAcclrt, DataAcclrtDec(1, :), axeTimeAcclrt, hightDigit,...
    axeTimeAcclrt, incor1, axeTimeAcclrt, incor2, 'LineWidth', 2);
title('����������� ������������ ������� ���� ��������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('�������� ���������', '������� �����', '�������� ������� ����� 1', '�������� ������� ����� 2');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);
figure(2);
plot(axeTimeAcclrt, DataAcclrtDec(1, :), axeTimeAcclrt, counter,...
    axeTimeAcclrt, hightAndLowCounter, 'LineWidth', 2);
title('����������� ������������ ������� ���� ��������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('�������� ���������', '������� �� 16 ��������', '������� ����� � ��.�.��������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);