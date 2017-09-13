clc
clear all
%�������� �����
[InFileName, InPath] = uigetfile('*.bit','�������� ���� ��� A-�����', ...
    'D:\work\telemetry\trident\');
if isequal(InFileName, 0)
   disp('����� ����� �������.')
   break
else
   disp(['������ ����: ', fullfile(InPath, InFileName), '.'])
end
%������ ����� ���
disp('�������� �����.')
InFID = fopen(fullfile(InPath, InFileName), 'r');
InData = fread(InFID, 'int8');%������ ������� ������
fclose(InFID);
clear InFID
% %������ ��� � ������
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
forDisp = 0.01;
for i = 4:1:size(InData, 1)
    %����� ������
    if (abs(InData(i - 3) - 13) <= 2) && (abs(InData(i - 2) + 75) <= 2) && ...
            (abs(InData(i - 1) - 115) <= 2) && (syncFound == 0)
        syncFound = 1;
        frameCnt = frameCnt + 1;
    end
    %���������� �������
    if syncFound == 1
        GTS(frameCnt, : ) = InData((i - 3):1:(i + 356));
        syncFound = 0;
        i = i + 353; %#ok<FXSET>
    end
    %����� ���������
    if ((i*100/size(InData, 1)) > forDisp)
        disp(['������� ��������: ', num2str(i*100/size(InData, 1)), '%.']);
        forDisp = forDisp + 0.01;
        disp(['���� ' num2str(frameCnt)]);
    end
end
clear frameCnt syncFound wordInd
%���������� �����������
save(fullfile(InPath, [InFileName '.mat']));
% ����� ������������ ���������
disp('����� ������������ ���������.');
value = 0;
valCount = 0;
countPeriod = 0;
numAccelParts = 0;
for i = 1:1:size(GTS, 2)
    for j = 1:1:8000
        if GTS(j, i) == value && valCount <= 40
            valCount = valCount + 1;
        elseif (40 - valCount) <= 1
            valCount = 0;
            value = GTS(j, i);
            countPeriod = countPeriod + 1;
        else
            valCount = 0;
            value = GTS(j, i);
        end
    end
    if countPeriod > 200
        disp(['����� : ', num2str(i + 3), '.']);
        countPeriod = 0;
        numAccelParts = numAccelParts + 1;
        accelParts(numAccelParts, : ) = GTS(:, i );
        numbersOfParts(numAccelParts) = i;
    end
end
