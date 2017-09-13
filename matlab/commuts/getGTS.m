%% ������ ����� ������
clc;
clear;
disp('������ ������ �� �����...');
data = filereader('uint8');
data = data';
fpathMAT = uigetdir('e:\MATscripts\', '�������� ������� ��� ���������� �����������');
disp('������ ������ ���������.');
disp('���������� ������...');
save([fpathMAT '\' 'data_raw.mat'], 'data', 'fpathMAT');
disp('���������� ������ ���������.');

%% ����� ��� � �����
disp('������ ���...');
dataRev = reversBit(data, 8);
disp('������ ��� ��������.');
disp('���������� ������...');
save([fpathMAT '\' 'data_revers.mat'], 'dataRev', 'fpathMAT');
disp('���������� ������ ���������.');

%% ��������� ������ � ������� ����
disp('�������������� � ������� ���...');
dataBit = convertToBits(dataRev, 8);
disp('�������������� ���������.');
disp('���������� ������...');
save([fpathMAT '\' 'data_bits.mat'], 'dataBit', 'fpathMAT');
disp('���������� ������ ���������.');

%% ������������ ��� � ������� ����
disp('�������������, ������������ � ������������ ��� � ������� ����...');
lenFrame = 2880;
lenSinhr = 24;
porogHem = 3;
sinhra = '0x0db573';
dataSinhr = formBitGTS(dataBit, lenFrame, lenSinhr, sinhra, porogHem);
disp('������������ ��� � ������� ���� ���������.');
disp('���������� ������...');
save([fpathMAT '\' 'data_sinhr.mat'], 'dataSinhr', 'fpathMAT');
disp('���������� ������ ���������.');

%% �������������� � ���
disp('�������������� � ����� ���...');
lenWord = 8;
GTS = formChanelsGTS(dataSinhr, lenWord);
disp('��� �����������...');
disp('���������� ������...');
save([fpathMAT '\' 'GTS_A.mat'], 'GTS', 'fpathMAT');
disp('���������� ������ ���������.');

%%
