function [fullBaseTMPFName, baseTMPFName, baseTMPData] = ...
    FOpenBaseTMP(fileTypeTMP, defDir)
%% ����� �����
[baseTMPFName, pathBaseTMP] = uigetfile(...
    [defDir, '\baseTMP\*.tlm'],...
    '�������� ���� � ������� ���');

%% �������� �����
if isequal(baseTMPFName, 0)
    display('������.');
    display('���� � ������� ��� �� ������.');
    return
else
    fullBaseTMPFName = fullfile(pathBaseTMP, baseTMPFName);
    display(['������ ����: ' fullBaseTMPFName]);
    clear pathBaseTMP
end

%% �������� �����
baseTMPFID = fopen(fullBaseTMPFName, 'r');
baseTMPData = fread(baseTMPFID, fileTypeTMP);
fclose(baseTMPFID);
clear baseTMPFID
end