function [win, winBef, winAft, maxProbVal] = getWinSize(s, stepWin)
%GETWINSIZE Функция определения оптимальных размеров окна
%   участка до скачка и участка после скачка
maxWin = length(s);
lenWinCur = stepWin : stepWin : maxWin;
lenWinBef = stepWin / 2 : stepWin / 2 : maxWin - stepWin / 2;
maxProb = zeros(length(lenWinCur), length(lenWinBef));

numTestWin = length(lenWinCur);
numTestBef = length(lenWinBef);
numTest = numTestWin * numTestBef;
j = 0;
for i_lw = 1:1:length(lenWinCur)
    for i_lwb = 1:1:length(lenWinBef)
        if lenWinCur(i_lw) - lenWinBef(i_lwb) < 2
            j = j + 1;
            continue;
        end
        lenWinAft = lenWinCur(i_lw) - lenWinBef(i_lwb);
        maxProb(i_lw, i_lwb) = ...
            max(get_probability(s, lenWinBef(i_lwb), lenWinAft));
        j = j + 1;
        disp(['\rТест (' num2str(numTestWin) ' : ' num2str(numTestBef) ...
            '): ' num2str(j) '/' num2str(numTest)])
        
    end
end
end

