function data = filereader(type)
[fname, fpath] = uigetfile('*.*', '�������� ����', ...
    'e:\fedorenko_ns\work\telemetry\trident\');
if isequal(fname, 0)
   disp('����� ����� �������.');
   return
else
   disp(['������ ����: ', fullfile(fpath, fname), '.']);
end
dataFID = fopen(fullfile(fpath, fname), 'r');
data = fread(dataFID, type);
fclose(dataFID);
if (length(data) < 3)
    disp('������� ��������� ����.');
    return
end
clear dataFID fname fpath
end