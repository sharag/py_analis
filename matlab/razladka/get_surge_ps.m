function [s, sInd] = get_surge_ps(len0, lenS, skvaj, num_s)
%GET_SURGE_PS —качок посто€нной составл€ющей
% len0 - определ€ет длину нулевого участка
% lenS - длина скачка
% skvaj - коэффициент - часть null_len между скачками
% num_s - количество скачков
    s = zeros(1, floor(len0 * skvaj));
    sInd = zeros(0);
    n = num_s;
    while n > 0
        n = n - 1;
        % 1
        sInd = [sInd, length(s) + 1 : 1 : (length(s) + lenS)];
        s = [s, ones(1, lenS)];
        % 0
        s = [s, zeros(1, floor(len0 * skvaj))]; %#ok<*AGROW>
    end
end
