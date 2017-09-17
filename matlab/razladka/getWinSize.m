function [win, winBef, winAft, maxProbVal] = getWinSize(s, stepWin)
%GETWINSIZE ������� ����������� ����������� �������� ����
%   ������� �� ������ � ������� ����� ������
    maxWin = length(s) - stepWin;
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


        end
        disp(['���� (' num2str(numTestWin) ' : ' num2str(numTestBef) ...
            '): ' num2str(j) '/' num2str(numTest)])
    end
    [M, ind] = max(maxProb(:));
    [indRow, indCol] = ind2sub(size(maxProb), ind);
    % ������������ �������� ����������
    win = lenWinCur(indRow);
    winBef = lenWinBef(indCol);
    winAft = win - winBef;
    maxProbVal = M;
end

