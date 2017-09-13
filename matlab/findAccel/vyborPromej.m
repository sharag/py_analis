clc;
clear;

freqFrame = 400; %������� ���������� �������� � �������
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
proizv = zeros(1,length(Data)-1);
for i=2:length(Data)
    proizv(i-1) = Data(i) - Data(i-1);
end
axeTimeProizv = axeTime;
axeTimeProizv(length(axeTimeProizv)) = [];

figure;
plot(axeTime, Data, axeTimeProizv, (proizv+1000), 'LineWidth', 2);
title('��������� � �����������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);

skoProizv = zeros(1,length(proizv)-freqFrame);
MOProizv = zeros(1,length(proizv)-freqFrame);
for i=1:length(skoProizv)
    skoProizv(i) = std(proizv(i:i+freqFrame));
    MOProizv(i) = mean(proizv(i:i+freqFrame));
end

figure
plot(stepTime:stepTime:length(skoProizv)*stepTime,skoProizv,...
    stepTime:stepTime:length(skoProizv)*stepTime, MOProizv, 'LineWidth', 2);
title('��� � �� �����������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
