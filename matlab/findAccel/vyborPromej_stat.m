function vyborPromej_stat()
%clc;
%clear;

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
proizv = zeros(1,length(Data)-1);
for i=2:length(Data)
    proizv(i-1) = Data(i) - Data(i-1);
end
skoData = zeros(1,length(Data)-freqFrame*3);
MOData = zeros(1,length(Data)-freqFrame*3);
for i=1:length(skoData)
    skoData(i) = std(Data(i:i+freqFrame*3));
    MOData(i) = mean(Data(i:i+freqFrame*3));
end
skoProizv = zeros(1,length(proizv)-freqFrame);
MOProizv = zeros(1,length(proizv)-freqFrame);
for i=1:length(skoProizv)
    skoProizv(i) = std(proizv(i:i+freqFrame));
    MOProizv(i) = mean(proizv(i:i+freqFrame));
end

figure;subplot(4,1,1);
plot(stepTime:stepTime:length(Data)*stepTime, Data, 'LineWidth', 2);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(4,1,2);
plot(stepTime:stepTime:length(proizv)*stepTime, proizv, 'LineWidth', 2);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(4,1,3);
plot(stepTime:stepTime:length(skoProizv)*stepTime, skoProizv, 'LineWidth', 2);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(4,1,4);
plot(stepTime:stepTime:length(MOProizv)*stepTime, MOProizv, 'LineWidth', 2);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);