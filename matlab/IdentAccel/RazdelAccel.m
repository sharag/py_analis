clc;
clear;
%���������
decimaVal = 1;%���������� ������������� �������� � ������� ���������
fqFrAcclrt = 400;%������� ���������� �������� � �������
%������������� ����������
fqFrAcclrt = fqFrAcclrt/decimaVal;%������� ���������� �������� � �������
stepTimeAcclrt = 1/fqFrAcclrt;%��� ��������� ����� � ������ ���������
clear fqFrAcclrt
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
%������������ ������ ���������
accelPartsLow = zeros(3, size(DataAcclrt, 2));
accelPartsHight = zeros(3, size(DataAcclrt, 2));
accelPartsHight(1, :) = fix(DataAcclrt(1, :)./256);
accelPartsHight(2, :) = fix(DataAcclrt(2, :)./256);
accelPartsHight(3, :) = fix(DataAcclrt(3, :)./256);
accelPartsLow(1, :) = mod(DataAcclrt(1, :), 256);
accelPartsLow(2, :) = mod(DataAcclrt(2, :), 256);
accelPartsLow(3, :) = mod(DataAcclrt(3, :), 256);
disp('������������ ��������� ��������� �� �����.');
save([PathFNameDataA0 '..\accelParts.mat']);
clear PathFNameDataA0
% ����������
transitStat = zeros(3, 3, 2);
for i = 1:1:3
    for j = 1:1:size(DataAcclrt, 2)
        if (j >= 2) && (accelPartsHight(i, j) ~= accelPartsHight(i, j-1));
            for k = 1:1:3
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