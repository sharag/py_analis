function [fullBaseTMPFName, baseTMPFName, baseTMPData] = ...
    FOpenBaseTMP(fileTypeTMP, defDir)
%% Выбор файла
[baseTMPFName, pathBaseTMP] = uigetfile(...
    [defDir, '\baseTMP\*.tlm'],...
    'Выберите файл с базовым ТМП');

%% Проверка файла
if isequal(baseTMPFName, 0)
    display('Ошибка.');
    display('Файл с базовым ТМП не выбран.');
    return
else
    fullBaseTMPFName = fullfile(pathBaseTMP, baseTMPFName);
    display(['Выбран файл: ' fullBaseTMPFName]);
    clear pathBaseTMP
end

%% Открытие файла
baseTMPFID = fopen(fullBaseTMPFName, 'r');
baseTMPData = fread(baseTMPFID, fileTypeTMP);
fclose(baseTMPFID);
clear baseTMPFID
end