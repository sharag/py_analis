function [files, pathTMP] = FOpenDirFunc(defDir)
%% ����� ��������
pathTMP = uigetdir([defDir '\Data\funkcional\'], '�������� ������� � �������������� ���');
if pathTMP == 0
    display('������.');
    display('�� ������ ������� ��� ���������� �����������.');
    return
else
    pathTMP = [pathTMP '\'];
    display(['������� � �������������� ���: ' pathTMP]);
end
files = dir([pathTMP '*.tlm']);
if length(files) < 1
    display('������.');
    display('������� �� �������� ������������� ���');
    return
end
end