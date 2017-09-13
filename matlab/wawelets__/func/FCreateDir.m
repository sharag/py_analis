function [pathRez, pathData] = FCreateDir(defDir)
pathRez = [defDir '\Results\'];
mkdir(pathRez);
display(['Каталог для сохранения результатов: ' pathRez]);
pathData = [defDir '\Data\'];
mkdir(pathData);
display(['Каталог для сохранения промежуточных данных' pathData]);
end