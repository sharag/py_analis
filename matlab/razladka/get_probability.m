function [ prob ] = get_probability( s, winBef, winAft )
%GET_PROBABILITY ‘ункци€ вычислени€ отношени€ правдоподоби€
% s - входной массив, тип list
% winBef - длина окна до скачка
% winAft - длина окна после скачка

% ‘ормирование массива дл€ хранени€ значений отношени€ правдободоби€ скольз€щего окна
prob = zeros(1, length(s) - winBef - winAft);
for i = 1 : 1 : length(s) - winBef - winAft
    % ћатематическое ожидание окна до скачка
    meanBef = mean(s(i : i + winBef));
    % ћатематическое ожидание окна после скачка
    meanAft = mean(s(i + winBef : i + winBef + winAft));
    % ƒисперси€ всего окна
    varAll = var(s(i : i + winBef + winAft));
    if varAll == 0
        varAll = 0.000000001;
    end
    % ѕодсчет суммы дл€ отношени€ правдободоби€
    summ = 0;
    for j = 1 : 1 : winAft
        summ = summ + ...
            (s(i + winBef + j) - meanBef - (meanAft - meanBef) / 2);
    end
    % –асчет отношени€ правдоподоби€
    prob(i) = (meanAft - meanBef) * summ / varAll;
end

end

