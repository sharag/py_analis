clc;
clear;

freqFrame = 100; %������� ���������� �������� � �������
stepTime = 1/freqFrame; %��� ��������� ����� � ������ ���������
clear fqFrAcclrt

[FNameData, PathFNameData] = uigetfile({'*.*', '���� ���'}, ...
    '�������� ���� ���', 'E:\MATscripts\findAccel\');
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
    fclose(FIDData);
    exit;
end

Data = medfilt1(Data,3);
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

figure;subplot(3,1,1);
plot(axeTime, Data, 'LineWidth', 2);
title('��������� 1', 'FontName', 'Times New Roman',...
    'FontSize', 10);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);





[FNameData, PathFNameData] = uigetfile({'*.*', '���� ���'}, ...
    '�������� ���� ���', 'E:\MATscripts\findAccel\');
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
    fclose(FIDData);
    exit;
end

Data = medfilt1(Data,3);
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

subplot(3,1,2);
plot(axeTime, Data, 'LineWidth', 2);
title('��������� 2', 'FontName', 'Times New Roman',...
    'FontSize', 10);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);





[FNameData, PathFNameData] = uigetfile({'*.*', '���� ���'}, ...
    '�������� ���� ���', 'E:\MATscripts\findAccel\');
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
    fclose(FIDData);
    exit;
end

Data = medfilt1(Data,3);
axeTime = (0:stepTime:(length(Data)*stepTime)-stepTime)';

subplot(3,1,3);
plot(axeTime, Data, 'LineWidth', 2);
title('��������� 3', 'FontName', 'Times New Roman',...
    'FontSize', 10);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

