%% �������-������
% ����������� ������������ ��������� ��������� ��� ������������ ��������
clc
clear

%% �������� ���������
defDir = 'g:\fedorenko_ns\MATscripts\wawelets\optimumWaweletForAccel';
defDir = uigetdir(defDir, '�������� ������� � ��������');
% �������� �������� � ������������ ������������
% � ��� ������������� ������
[pathRez, pathData] = FCreateDir(defDir); 

%% �������� ���������
fileTypeTMP = 'int16'; % ��� ������
freqDiskrData = 100; % ������� ���������� �������� � �������
dScale = 0.8; %�������� ��������� � �����

%% �������� ������
% �������� ����� � ������� ���������
TMPFName = 'g:\fedorenko_ns\MATscripts\wawelets\baseTMP\T2-1d.bit.20.D1_A.tlm';
if isequal(TMPFName, 0)
    display('������.');
    display('���� � ��� ������ ��������� �� ������.');
    return
else
    display(['���� ������ ���������: ' TMPFName]);
end
TMPFID = fopen(TMPFName, 'r');
TMPData = fread(TMPFID, fileTypeTMP);
fclose(TMPFID);
clear TMPFID
% �������� ����� � ��� "������"
ModeFName = 'g:\fedorenko_ns\MATscripts\wawelets\baseTMP\T2-1d.bit.14.D4.tlm';
if isequal(ModeFName, 0)
    display('������.');
    display('���� � ��� "������" �� ������.');
    return
else
    display(['���� ��� "������": ' ModeFName]);
end
ModeFID = fopen(ModeFName, 'r');
ModeData = fread(ModeFID, fileTypeTMP);
fclose(ModeFID);
clear ModeFID
% ������
figure;
TMPName = '������ ��������� � ������ �������';
Message = '������� ������ ��������� � ��� "������"';
TMPAxeX = (1/freqDiskrData:1/freqDiskrData:length(TMPData)/freqDiskrData)';
set(gcf, 'Name', TMPName, 'ToolBar', 'figure');
plot(TMPAxeX, TMPData, TMPAxeX, ModeData, 'LineWidth', 2);
title(Message, 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
legend('������ ���������', '��� "������"');
save([pathRez 'WData.mat']);

%% ���������� ��������
clc
clear
load('g:\fedorenko_ns\MATscripts\wawelets\optimumWaweletForAccel\Results\WData.mat')
scale = 350;
event = 6235;

% �������� ��� ���������
DataTemp = medfilt1(TMPData(1000:12300), 10);

% �������� � ������� ��������
meanData = mean(DataTemp);
DataTemp0 = DataTemp - meanData;

% ������������� ��� � ������� ��������
diapazon = max(DataTemp0) - min(DataTemp0);
DataTempNorm = (DataTemp0 - max(DataTemp0) + diapazon/2)./(diapazon/2);
clear diapazon meanData

save([pathRez 'WData1.mat']);

clc
clear
load('g:\fedorenko_ns\MATscripts\wawelets\optimumWaweletForAccel\Results\WData1.mat')

lengthWawe = 800;
stepWawe = 10;
sum = 0;
% ����������� ���������� �������� 
for i = 1:1:(lengthWawe/stepWawe)  %������ ��������
    for j = 1:1:i+1  %�������� ������ �������� �� �������
        sum=sum+1;
    end
end
numIter = sum;
sum = 0;

for i = 1:1:(lengthWawe/stepWawe)  %������ ��������
    for j = 1:1:i+1  %�������� ������ �������� �� �������
        ii = i*stepWawe;
        jj = j*stepWawe;
        beginPart = event-jj; % ��������� ������ �������� ��������� ��-���������
        endPart = beginPart+ii; % ��������� ����� �������� ��������� ��-���������
        % ����� �������� ���������
        WaweData = TMPData(beginPart:1:endPart);
        % ��������� ��������
        [psi_WData, xval_WData, nc_WData] = pat2cwav(WaweData', 'polynomial', 60, 'continuous');
        % �������-��������������
        % �������� ��� ���������
        Sc = cwt(DataTemp, scale, psi_WData);
        Mmax(i,j) = max(max(Sc));
        Mmean(i,j) = mean(mean(Sc));
        
        % �������� � ������� ��������
        Sc = cwt(DataTemp0, scale, psi_WData);
        Mmax0(i,j) = max(max(Sc));
        Mmean0(i,j) = mean(mean(Sc));
        
        % ������������� ���
        Sc = cwt(DataTempNorm, scale, psi_WData);
        MmaxNorm(i,j) = max(max(Sc));
        MmeanNorm(i,j) = mean(mean(Sc));
        
        sum = sum + 1;
        if sum/10 == fix(sum/10)
            display(['���������:' num2str(sum*100/numIter) '%']);
        end
    end
end
clear i j ii jj Sc psi_WData xval_WData nc_WData sum numIter stepWawe beginPart endPart scale

save([pathRez 'WData2.mat']);

% 
% 