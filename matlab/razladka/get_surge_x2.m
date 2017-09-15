function [ s, sInd ] = get_surge_x2( len0, lenS, skvaj, num_s )
%GET_SURGE_X2 Кратковременный скачок c линейным изменением значений
% null_len - определяет длину нулевого участка
% surge_len - длина скачка
% skvaj - коэффициент - часть null_len между скачками
% n_surge - количество скачков
    s = zeros(1, floor(len0 * skvaj));
    sInd = zeros(0);
    n = num_s;
    lenS4 = floor(lenS / 4); % Четвертая часть скачка
    signAdd = false;
    while n > 0
        n = n - 1;
        % 1
        sInd = [sInd, length(s) + 1 : 1 : (length(s) + lenS)];
        s = [s, (((1 : 1 : lenS4) ./ lenS4) .^ 2) ./ 2 ];
        s = [s, (1 - (((1 : 1 : lenS4) - lenS4) ./ lenS4) .^ 2) ./ 2 + 0.5];
        if 2 * lenS4 < lenS /2
            s = [s, 1];
            signAdd = true;
        end
        s = [s, 1 - (((1 : 1 : lenS4) ./ lenS4) .^ 2 ./ 2)];
        s = [s, (((((1 : 1 : lenS4) - lenS4) ./ lenS4) .^ 2) ./ 2)];
        if signAdd
            if (4 * lenS4 + 1) < lenS
                s = [s, 0];
            end
            signAdd = false;
        else
            if 4 * lenS4 < lenS
                s = [s, 0];
            end
        end
        % 0
        s = [s, zeros(1, floor(len0 * skvaj))]; %#ok<*AGROW>
    end
end

