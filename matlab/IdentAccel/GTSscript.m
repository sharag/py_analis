clc
clear all
%�������� �����
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
        value = int8(InData(i));
        GTS(frameCnt, wordInd) = value; %#ok<*SAGROW>
        wordInd = wordInd + 1;
    end
    if wordInd == 357
        wordInd = 1;
        syncFound = 0;
    end
    %����� ���������
    if ((i/100000) == floor(i/100000))
        disp(['������� ��������: ', num2str(i*100/length(InData)), '%.']);
    end
end
%���������� �����������
save(fullfile(InPath, [InFileName '.mat']));