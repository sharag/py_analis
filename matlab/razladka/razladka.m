%% ��������
% ������ ������������ ��������

%% �������������� ������������
null_len = 100;  % ����� ��������� �������
k_surge = 0.5;  % ����������� ��������� ����� ���������� ���� � ����� ������
skvaj = 1;  % ���������� ������������������ ������� (1 - ����� �������� null_len)
n_surge = 3;  % ���������� �������
surge_len = floor(null_len*k_surge);  % ����� ������
step_win = 10;  % ��� ��������� ���� (������� 2)
num_order = 16;  % ���������� �������� �������� ��� ����� ����������� ������
num_test = 10;  % ���������� ������������� ��� ������� �������� ����������� ������
koef_porog_ = 0.9;  % ��������� �������� ��� �����������, ������������ ���� �� ��������� ��������� �������������

%% ������������ �������

[surge_ps, surge_ps_ind] = get_surge_ps(null_len, surge_len, skvaj, n_surge);
[surge_x1, surge_x1_ind] = get_surge_x1(null_len, surge_len, skvaj, n_surge);
[surge_x2, surge_x2_ind] = get_surge_x2(null_len, surge_len, skvaj, n_surge);
%surge_ps, surge_lin, surge_kvadr, surge_highcos = get_surge_ps(null_len, surge_len, skvaj, n_surge);

