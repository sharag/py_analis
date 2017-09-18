%% ��������
% ������ ������������ ��������
clc
clear

%% �������������� ������������
len0 = 100;  % ����� ��������� �������
kSurge = 0.5;  % ����������� ��������� ����� ���������� ���� � ����� ������
skvaj = 1;  % ���������� ������������������ ������� (1 - ����� �������� null_len)
num_s = 3;  % ���������� �������
sLen = floor(len0*kSurge);  % ����� ������
stepWin = 10;  % ��� ��������� ���� (������� 2)
numOrder = 16;  % ���������� �������� �������� ��� ����� ����������� ������
numTest = 10;  % ���������� ������������� ��� ������� �������� ����������� ������
koefPorog = 0.9;  % ��������� �������� ��� �����������, ������������ ���� �� ��������� ��������� �������������

%% ������ ������������ ������ � ���������� �� ����������� �������
Posh = [0.0001 : 0.0001 : 0.001, 0.001 : 0.001 : 0.01, 0.01 : 0.01 : 0.02];
Posh = Posh * numOrder;

%% ������������ �������

[surge_ps, surge_ps_ind] = ...
    get_surge_ps(len0, sLen, skvaj, num_s);
[surge_x1, surge_x1_ind] = ...
    get_surge_x1(len0, sLen, skvaj, num_s);
[surge_x2, surge_x2_ind] = ...
    get_surge_x2(len0, sLen, skvaj, num_s);
[surge_hcos, surge_hcos_ind] = ...
    get_surge_hcos(len0, sLen, skvaj, num_s);

%% ������ ���� � ���������� ������� ��������� �������������
signal = surge_ps;
% ����� ���������� ����, ������ �������� ������� ��������� �������������
[win, winBef, winAft, maxProbVal] = getWinSize(signal, stepWin);
porog = koefPorog * maxProbVal;
% ������ ������� ��������� �������������
probability = get_probability( signal, winBef, winAft );

%% ������������ ������������� �������������

numPO = zeros(0);
numLT = zeros(0);
numPC = zeros(0);



