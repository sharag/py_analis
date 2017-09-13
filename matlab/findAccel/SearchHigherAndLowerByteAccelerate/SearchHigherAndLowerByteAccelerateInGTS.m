clc;
clear;
%���������
decimaVal = 1;%���������� ������������� �������� � ������� ���������
fqFrAcclrt = 400;%������� ���������� �������� � �������
%������������� ����������
fqFrAcclrt = fqFrAcclrt/decimaVal;%������� ���������� �������� � �������
stepTimeAcclrt = 1/fqFrAcclrt;%��� ��������� ����� � ������ ���������
clear fqFrAcclrt
%������ ������
[InFileName, InPath] = uigetfile('*.bit','�������� ���� ��� A-�����', ...
    'D:\work\telemetry\trident\');
if isequal(InFileName, 0)
   disp('����� ����� �������.')
else
   disp(['������ ����: ', fullfile(InPath, InFileName), '.'])
end
%������ ����� ���
disp('�������� �����.')
InFID = fopen(fullfile(InPath, InFileName), 'r');
InData = fread(InFID, 'uint8');%������ ������� ������
fclose(InFID);
clear InFID
disp('������ ����� ���������.')
%������ ��� � ������
% disp('������ ��� � ������.')
% x = 0:1:255;
% xx = bitrevorder(x);
% for i = 1:1:length(InData)
%     InData(i) = xx(InData(i) + 1);
% end
% clear x xx
% %������ ����� � �������� ���
% RevFID = fopen(fullfile(InPath, [InFileName '.rev.bit']), 'w');
% fwrite(RevFID, InData, 'uint8');%������ ������� ������
% fclose(RevFID);
% clear RevFID
%���������� ���
disp('���������� ���.')
syncFound = 0;
frameCnt = 0;%������ �� ������
wordInd = 1;%������ �� ������
for i = 1:1:length(InData)
    %����� ������
    if (i > 3) && (InData(i - 3) == 13) && (InData(i - 2) == 181) && ...
            (InData(i - 1) == 115) && (syncFound == 0)
        syncFound = 1;
        frameCnt = frameCnt + 1;
    end
    %���������� �������
    if syncFound == 1
        GTS(frameCnt, wordInd) = int8(InData(i)); %#ok<*SAGROW>
        wordInd = wordInd + 1;
    end
    if wordInd == 358
        wordInd = 1;
        syncFound = 0;
    end
    %����� ���������
    if ((i/10000) == floor(i/10000))
        disp(['������� ��������: ', num2str(i*100/length(InData)), '%.']);
    end
end
clear wordInd frameCnt syncFound
%���������� �����������
save(fullfile(InPath, [InFileName '.mat']));

%//////////////////////////////////////////////////////////////////////////

%�������� ������� ����������
%�������� ����� ������� �������
[wrkSpcFileName, wrkSpcPath] = uigetfile('*.mat','�������� ���� ������� ������� (workspace)', ...
    'D:\work\telemetry\trident\');
if isequal(wrkSpcFileName, 0)
   disp('����� ����� workspace �������.')
else
   disp(['������ ���� workspace: ', fullfile(wrkSpcPath, wrkSpcFileName), '.'])
end
load(fullfile(wrkSpcPath, wrkSpcFileName));
disp('���� ������� ������ ��������.')


sostNum = 3;
% ����������
transitStat = zeros(sostNum, sostNum, 2);
for i = 1:1:sostNum
    for j = 1:1:size(DataAcclrt, 2)
        if (j >= 2) && (accelPartsHight(i, j) ~= accelPartsHight(i, j-1));
            for k = 1:1:sostNum
                transitStat(i, k, 1) = transitStat(i, k, 1) + 1;
                if (abs(accelPartsLow(k, j) - accelPartsLow(k, j-1)) > 224)
                    transitStat(i, k, 2) = transitStat(i, k, 2) + 1;
                end
            end
        end
    end
end
razn = transitStat(:, :, 1) - transitStat(:, :, 2);
x = transitStat(:,:,1);
xx = transitStat(:,:,2);

%��� ������� ��� ���������
axeTimeAcclrt = (0:stepTimeAcclrt:...
    (size(DataAcclrt, 2)*stepTimeAcclrt)-stepTimeAcclrt)';
clear stepTimeAcclrt

hightDigit = accelPartsHight(1, :).*256;
incor1 = hightDigit + accelPartsLow(3, :);
incor2 = hightDigit + accelPartsLow(1, :);

figure(1);
plot(axeTimeAcclrt, DataAcclrt(1, :), axeTimeAcclrt, hightDigit,...
    axeTimeAcclrt, incor1, axeTimeAcclrt, incor2, 'LineWidth', 2);
title('����������� ������������ ������� ���� ��������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('�������� ���������', '������� �����', '�������� ������� ����� 1', '�������� ������� ����� 2');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);


counter = zeros(1, size(DataAcclrt, 2));
dir = 1;
j = 1;
for i=1:1:size(DataAcclrt, 2)
    if (dir == 1) && ((i/40) == floor(i/40))
        j = j + 1;
    elseif (i/40) == floor(i/40)
        j = j - 1;
    end
    counter(i) = j;
    if j == 2^16
        dir = 0;
    elseif j == 0
        dir = 1;
    end
end

counterLow = mod(counter, 256);
hightAndLowCounter = hightDigit + counterLow;
figure(2);
plot(axeTimeAcclrt, DataAcclrt(1, :), axeTimeAcclrt, counter,...
    axeTimeAcclrt, hightAndLowCounter, 'LineWidth', 2);
title('����������� ������������ ������� ���� ��������', 'FontName', 'Times New Roman',...
    'FontSize', 14);
xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('�������� ���������', '������� �� 16 ��������', '������� ����� � ��.�.��������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);