function [pathRez, pathData] = FCreateDir(defDir)
pathRez = [defDir '\Results\'];
mkdir(pathRez);
display(['������� ��� ���������� �����������: ' pathRez]);
pathData = [defDir '\Data\'];
mkdir(pathData);
display(['������� ��� ���������� ������������� ������' pathData]);
end