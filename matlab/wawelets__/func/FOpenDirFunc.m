function [files, pathTMP] = FOpenDirFunc(defDir)
%% Выбор каталога
pathTMP = uigetdir([defDir '\Data\funkcional\'], 'Выберите каталог с анализируемыми ТМП');
if pathTMP == 0
    display('Ошибка.');
    display('Не указан каталог для сохранения результатов.');
    return
else
    pathTMP = [pathTMP '\'];
    display(['Каталог с анализируемыми ТМП: ' pathTMP]);
end
files = dir([pathTMP '*.tlm']);
if length(files) < 1
    display('Ошибка.');
    display('Каталог не содержит анализируемых ТМП');
    return
end
end