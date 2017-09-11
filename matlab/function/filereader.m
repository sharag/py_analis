function data = filereader(type)
[fname, fpath] = uigetfile('*.*', 'Выберите файл', ...
    'e:\fedorenko_ns\work\telemetry\trident\');
if isequal(fname, 0)
   disp('Выбор файла отменен.');
   return
else
   disp(['Выбран файл: ', fullfile(fpath, fname), '.']);
end
dataFID = fopen(fullfile(fpath, fname), 'r');
data = fread(dataFID, type);
fclose(dataFID);
if (length(data) < 3)
    disp('Слишком маленький файл.');
    return
end
clear dataFID fname fpath
end