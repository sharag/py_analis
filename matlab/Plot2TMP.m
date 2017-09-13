clc;
clear;
%���������
freqFrame1 = 100;%������� ���������� �������� � �������
freqFrame2 = 100;%������� ���������� �������� � �������
%������������� ����������
stepTime1 = 1/freqFrame1;%��� ��������� ����� � ������ ���������
stepTime2 = 1/freqFrame2;%��� ��������� ����� � ������ ���������
%������������ ��� ����������
koef1 = 1;%1;
koef2 = 1;%1/20;
%������ ������� �����
[FNameData1, PathFNameData1] = uigetfile({'*.*', '���� ���'}, ...
    '�������� ������ ���� � ���', ...
    'C:\Users\fedorenko\Desktop\��� ��������\TMSignals');
if isequal(FNameData1, 0)
   disp('����� ����� �������.');
   exit
else
   disp(['������ ����: ', fullfile(PathFNameData1, FNameData1), '.']);
end
FIDData1 = fopen(fullfile(PathFNameData1, FNameData1), 'r');
Data1 = fread(FIDData1, 'int16');%'float');
if (length(Data1) < 3)
    disp('������� ��������� ����.');
end
fclose(FIDData1);
%������ ������� �����
[FNameData2, PathFNameData2] = uigetfile({'*.*', '���� ���'}, ...
    '�������� ������ ���� � ���', ...
    'C:\Users\fedorenko\Desktop\��� ��������\TMSignals');
if isequal(FNameData2, 0)
   disp('����� ����� �������.');
   exit
else
   disp(['������ ����: ', fullfile(PathFNameData2, FNameData2), '.']);
end
FIDData2 = fopen(fullfile(PathFNameData2, FNameData2), 'r');
Data2 = fread(FIDData2, 'uint16');
if (length(Data2) < 3)
    disp('������� ��������� ����.');
end
fclose(FIDData2);
%��� ������� ��� ������� ���������
axeTime1 = (0:stepTime1:(length(Data1)*stepTime1)-stepTime1)';
%��� ������� ��� ������� ���������
axeTime2 = (0:stepTime2:(length(Data2)*stepTime2) - stepTime2)';

Data1 = Data1.*koef1;
Data2 = Data2.*koef2;

%���������� �������� ��������� ��������� � ������ ��������� �� ����������
figure;
plot(axeTime1, Data1, 'LineWidth', 2);
hold on;
plot(axeTime2, Data2, 'LineWidth', 2);
% for i = 2:length(axeTime2)
%     if Data2(i) ~= Data2(i - 1)
%         plot([axeTime2(i),axeTime2(i)],[0,5*10^4], 'b--', 'LineWidth', 2);
%     end
% end
title('������ ��������� � ������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);