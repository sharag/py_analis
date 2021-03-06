%% ��������� � �������������� ���������
clc
clear

x = -30:0.1:30; % ������������ ���������
y = x.^2.*sin(x); % ���������� �������
x = 1:1:length(y); % ������������ ��� �������

z = y(170:1:309); % ����� ��������� �������
xz_1 = 170:1:170 + length(z) - 1; % ������������ ��� ������� ��� z
xz_2 = 70:1:70 + length(z) - 1; % ������������ ��� ������� ��� z
xz_3 = 400:1:400 + length(z) - 1; % ������������ ��� ������� ��� z

% ������������ ����������� ��������� �������
for i = 1:1:length(z)
    z1(2*i - 1) = z(i);
    z1(2*i) = z(i);
end
clear i
xz1_1 = 140:1:140 + length(z1) - 1; % ������������ ��� ������� ��� z1
xz1_2 = 10:1:10 + length(z1) - 1; % ������������ ��� ������� ��� z1
xz1_3 = 300:1:300 + length(z1) - 1; % ������������ ��� ������� ��� z1

z2 = z(1:2:length(z));% ������������ ������� ��������� �������
xz2_1 = 180:1:180 + length(z2) - 1; % ������������ ��� ������� ��� z2
xz2_2 = 105:1:105 + length(z2) - 1; % ������������ ��� ������� ��� z2
xz2_3 = 365:1:365 + length(z2) - 1; % ������������ ��� ������� ��� z2

FGrafKorr(x, y, xz_1, xz_2, xz_3, z, xz1_1, xz1_2, xz1_3, z1, xz2_1, xz2_2,...
    xz2_3, z2);
