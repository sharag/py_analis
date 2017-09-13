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
clear i ii DataAcclrt
fqFrAcclrt = fqFrAcclrt/decVal;%������� ���������� �������� � �������
stepTimeAcclrt = 1/fqFrAcclrt;%��� ��������� ����� � ������ ���������
clear fqFrAcclrt
disp('��������� ������������ ��������� �����������.');

%������������ ������ ���������
accelPartsLow = zeros(sostNum, size(DataAcclrtDec, 2));
accelPartsHight = zeros(sostNum, size(DataAcclrtDec, 2));
accelPartsHight(1, :) = fix(DataAcclrtDec(1, :)./256);
accelPartsHight(2, :) = fix(DataAcclrtDec(2, :)./256);
accelPartsHight(3, :) = fix(DataAcclrtDec(3, :)./256);
accelPartsLow(1, :) = mod(DataAcclrtDec(1, :), 256);
accelPartsLow(2, :) = mod(DataAcclrtDec(2, :), 256);
accelPartsLow(3, :) = mod(DataAcclrtDec(3, :), 256);
disp('������������ ��������� ��������� �� �����.');
save([PathFNameDataA0 '..\accelParts.mat']);

% ���������� �� ������ ���
statLower = zeros(sostNum, 3);
statHight = zeros(sostNum, 3);
for i = 1:1:sostNum
    oldValLow = 0;
    oldValHight = 0;
    for j = 2:1:size(DataAcclrtDec, 2)
        oldValLow = accelPartsLow(i, j - 1);
        oldValHight = accelPartsHight(i, j - 1);
        if accelPartsLow(i, j) ~= oldValLow
            statLower(i, 1) = statLower(i, 1) + 1;
        end
        if accelPartsHight(i, j) ~= oldValHight
            statHight(i, 1) = statHight(i, 1) + 1;
        end
    end
    statLower(i, 2) = size(DataAcclrtDec, 2);
    statHight(i, 2) = size(DataAcclrtDec, 2);
    statLower(i, 3) = statLower(i, 1)/statLower(i, 2);
    statHight(i, 3) = statHight(i, 1)/statHight(i, 2);
end
clear oldValLow oldValHight



%                   �������
%
%     �       | ���������� | ���������� | ���������  ���������� ���������
% ������������ | ���������  |  ��������  |      � ���������� ��������
%              |            |            |
%     1        |    ��      |     ��     |              ZZ
%              |            |            |
%     2        |    ��      |     ��     |              ZZ
%              |            |            |
%     3        |    ��      |     ��     |              ZZ

% ���������� �� ����� ���
statLowerI = zeros(sostNum, 3);
statHightI = zeros(sostNum, 3);
for i = 1:1:sostNum
    oldValLow = 0;
    oldValHight = 0;
    for j = 1734:1:size(DataAcclrtDec, 2)
        oldValLow = accelPartsLow(i, j - 1);
        oldValHight = accelPartsHight(i, j - 1);
        if accelPartsLow(i, j) ~= oldValLow
            statLowerI(i, 1) = statLowerI(i, 1) + 1;
        end
        if accelPartsHight(i, j) ~= oldValHight
            statHightI(i, 1) = statHightI(i, 1) + 1;
        end
    end
    statLowerI(i, 2) = size(DataAcclrtDec, 2) - 1734;
    statHightI(i, 2) = size(DataAcclrtDec, 2) - 1734;
    statLowerI(i, 3) = statLowerI(i, 1)/statLowerI(i, 2);
    statHightI(i, 3) = statHightI(i, 1)/statHightI(i, 2);
end
clear oldValLow oldValHight

%��� ������� ��� ���������
% axeTimeAcclrt = (0:stepTimeAcclrt:...
%     (size(DataAcclrt, 2)*stepTimeAcclrt)-stepTimeAcclrt)';
% clear stepTimeAcclrt

% figure(1);
% plot(axeTimeAcclrt, DataAcclrt(1, :), axeTimeAcclrt, hightDigit,...
%     axeTimeAcclrt, incor1, axeTimeAcclrt, incor2, 'LineWidth', 2);
% title('����������� ������������ ������� ���� ��������', 'FontName', 'Times New Roman',...
%     'FontSize', 14);
% xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
% ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
% set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
% hlegeng = legend('�������� ���������', '������� �����', '�������� ������� ����� 1', '�������� ������� ����� 2');
% set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);
