clc;
clear;

%���������
freqFrame = 100;%������� ���������� �������� � �������

%������������� ����������
stepTime = 1/freqFrame;%��� ��������� ����� � ������ ���������
clear fqFrAcclrt

%������ ������
[FNameData, PathFNameData] = uigetfile({'*.*', '���� ���'}, ...
    '�������� ���� ���', 'C:\Users\fedorenko\Desktop\��� ��������\TMSignals');
if isequal(FNameData, 0)
   disp('����� ����� �������.');
   exit
else
   disp(['������ ����: ', fullfile(PathFNameData, FNameData), '.']);
end

FIDData = fopen(fullfile(PathFNameData, FNameData), 'r');
Data = fread(FIDData, 'int16');
if (length(Data) < 3)
    disp('������� ��������� ����.');
end
fclose(FIDData);

%��� ������� ��� ���������
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

%���������� �������� ��������� ��������� � ������ ��������� �� ����������
figure;
plot(axeTime, Data./10, 'LineWidth', 2);
title('������ ���������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);