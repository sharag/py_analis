%% ��������
% ������ ������������ ��������
clc
clear

%% �������������� ������������
len0 = 400;  % ����� ��������� �������
kSurge = 0.2;  % ����������� ��������� ����� ���������� ���� � ����� ������
skvaj = 1;  % ���������� ������������������ ������� (1 - ����� �������� null_len)
num_s = 3;  % ���������� �������
sLen = floor(len0 * kSurge);  % ����� ������
stepWin = 2;  % ��� ��������� ���� (������� 2)
numOrder = 16;  % ���������� �������� �������� ��� ����� ����������� ������
numTest = 100;  % ���������� ������������� ��� ������� �������� ����������� ������
koefPorog = 0.9;  % ��������� �������� ��� �����������, ������������ ���� �� ��������� ��������� �������������

%% ������ ������������ ������ � ���������� �� ����������� �������
Posh = [0.00005 : 0.00005 : 0.001, 0.001 : 0.0005 : 0.01, 0.01 : 0.005 : 0.03];
Posh = Posh * numOrder;

%% ������������ �������

[surge_ps, surge_ps_ind] = ...
    get_surge_ps(len0, sLen, skvaj, num_s);
surge_ps = surge_ps .* (2 ^ numOrder);
[surge_x1, surge_x1_ind] = ...
    get_surge_x1(len0, sLen, skvaj, num_s);
surge_x1 = surge_x1 .* (2 ^ numOrder);
[surge_x2, surge_x2_ind] = ...
    get_surge_x2(len0, sLen, skvaj, num_s);
surge_x2 = surge_x2 .* (2 ^ numOrder);
[surge_hcos, surge_hcos_ind] = ...
    get_surge_hcos(len0, sLen, skvaj, num_s);
surge_hcos = surge_hcos .* (2 ^ numOrder);

%% ������ ���� � ���������� ������� ��������� �������������
% ����� ���������� ����, ������ �������� ������� ��������� �������������
[win, winBef_ps, winAft_ps, maxProbVal] = getWinSize(surge_ps, stepWin);
% porog_ps = koefPorog * maxProbVal;
% ������ ������� ��������� �������������
% probability = get_probability( signal, winBef, winAft );

% ����� ���������� ����, ������ �������� ������� ��������� �������������
[win, winBef_x1, winAft_x1, maxProbVal] = getWinSize(surge_x1, stepWin);
% porog_x1 = koefPorog * maxProbVal;
% ������ ������� ��������� �������������
% probability = get_probability( signal, winBef, winAft );

% ����� ���������� ����, ������ �������� ������� ��������� �������������
[win, winBef_x2, winAft_x2, maxProbVal] = getWinSize(surge_x2, stepWin);
% porog_x2 = koefPorog * maxProbVal;
% ������ ������� ��������� �������������
% probability = get_probability( signal, winBef, winAft );

% ����� ���������� ����, ������ �������� ������� ��������� �������������
[win, winBef_hcos, winAft_hcos, maxProbVal] = getWinSize(surge_hcos, stepWin);
% porog_hcos = koefPorog * maxProbVal;
% ������ ������� ��������� �������������
% probability = get_probability( signal, winBef, winAft );

%% ������������ ������������� �������������

[ po_ps, lt_ps, pc_ps ] = ...
    getVer( surge_ps, surge_ps_ind, koefPorog, numTest, Posh, num_s, numOrder, winBef_ps, winAft_ps);

[ po_x1, lt_x1, pc_x1 ] = ...
    getVer( surge_x1, surge_x1_ind, koefPorog, numTest, Posh, num_s, numOrder, winBef_x1, winAft_x1);

[ po_x2, lt_x2, pc_x2 ] = ...
    getVer( surge_x2, surge_x2_ind, koefPorog, numTest, Posh, num_s, numOrder, winBef_x2, winAft_x2);

[ po_hcos, lt_hcos, pc_hcos ] = ...
    getVer( surge_hcos, surge_hcos_ind, koefPorog, numTest, Posh, num_s, numOrder, winBef_hcos, winAft_hcos);



