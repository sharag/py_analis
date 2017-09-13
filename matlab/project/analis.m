%% �������-������
% ����������� �������� ������������� ���
% ���������� ��������
clc
clear

%% �������� ���������
defDir = 'g:\fedorenko_ns\MATscripts\wawelets';
defDir = uigetdir(defDir, '�������� ������� � ��������');
% �������� �������� � ������������ ������������
% � ��� ������������� ������
[pathRez, pathData] = FCreateDir(defDir); 

%% �������� ���������
fileTypeTMP = 'int16'; % ��� ������
freqDiskrData = 100; % ������� ���������� �������� � �������
dScale = 0.15; %�������� ��������� � �����

%% ���������� ��������
beginPart = 5900; % ��������� ������ �������� ��������� ��-���������
endPart = 6250; % ��������� ����� �������� ��������� ��-���������
% �������� ����� � ������� ���
[fullBaseTMPFName, baseTMPFName, baseTMPData] = FOpenBaseTMP(fileTypeTMP, defDir);
% ���������� ������� �������� ��� � ����� ������������ ���������
FGrafBaseTMP(baseTMPData, baseTMPFName);
% ���� ������� �������� ������ � ����� �������� ���������
[beginPart, endPart] = FScopePart(beginPart, endPart);
centrOfPart = floor(beginPart + (endPart - beginPart)/2);
% ����� �������� ���������
WaweData = baseTMPData(beginPart:1:endPart);
WaweData = WaweData - mean(WaweData);
% ��������� ��������
%[psi_WData, xval_WData, nc_WData] = pat2cwav(WaweData, 'orthcost', 3, 'continuous');%'polynomial', 10, 'continuous');
[psi_WData, xval_WData, nc_WData] = pat2cwav(WaweData', 'polynomial', 60, 'continuous');
% ���������� ������� ������������ ��������
FGrafBuildW(WaweData, psi_WData, freqDiskrData);
% ���������� ����������� ���������� ��������
save([pathRez 'WData.mat']);
save([pathRez 'Data.mat'], 'baseTMPData');
%% �������-������ ������ �������������� ���
% �������� ����������
if ~exist('defDir', 'var')
    defDir = uigetdir('g:\fedorenko_ns\MATscripts\wawelets', '�������� ������� � ��������');
end
load([defDir '\Results\WData.mat']);
% ������������ ����� ��������
scale = length(psi_WData) - dScale*length(psi_WData):1:length(psi_WData) + dScale*length(psi_WData);
% �������� �������� � �������������� ���
[files, pathTMP] = FOpenDirFunc(defDir);


for nfile = 1:1:length(files)
    % ������ ���������� � ����� ���
    infoFID = fopen([pathTMP, files(nfile).name '.txt'], 'r');
    fileType = fscanf(infoFID, '%s'); 
    fclose(infoFID);
    % ������ ����� ���
    infileID = fopen([pathTMP, files(nfile).name], 'r');
    DataNois = fread(infileID, fileType);
    fclose(infileID);
    % ����� ������������ ���������
%     Data = DataNois((beginPart - 2*freqDiskrData):(endPart + 2*freqDiskrData));
    Data = DataNois(16880:length(DataNois));%������ �� ���� ���
    % ���������� ������
    Data = medfilt1(Data, 30);
    DataTemp = Data(5:length(Data) - 5);
%     DataTemp = Data;
    clear Data
    % ���������� �� ������� ����������
%     shift = 0;
%     for i = 2:1:length(DataTemp)
%         if DataTemp(i - 1) - DataTemp(i) > (2^15 + 2^14 + 2^13)
%             shift = shift + 2^16;
%         elseif DataTemp(i) - DataTemp(i - 1) > (2^15 + 2^14 + 2^13)
%             shift = shift - 2^16;
%         end
%         Data(i) = DataTemp(i) + shift;
%     end
    Data = DataTemp; %���� ��������� �� �����
    clear DataTemp
    % ������������ ���������������� ���������
    meanData = mean(Data);
    Data = Data - meanData;
    % ���������� ������������ ��������� ������
%     DataTemp = zeros(1, 4001 + length(Data));
%     DataTemp(2001:2001 + length(Data) - 1) = Data(:);
    
    % ������������ ���������
    maxData = abs(max(DataTemp));
    minData = abs(min(DataTemp));
    if maxData > minData
        Data = DataTemp./maxData;
    else
        Data = DataTemp./minData;
    end
    clear DataTemp
    %
    plot(Data)
    % �������-�������������� �������
    Sc = cwt(Data, scale, psi_WData);
    
    ScMax(nfile) = max(max(Sc));
    ScMin(nfile) = min(min(Sc));
    ScMean(nfile) = mean(mean(Sc));

    disp([num2str(nfile*100/length(files)) ' %']);
end
