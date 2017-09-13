function [surge_ps, surge_ps_ind] = get_surge_ps(null_len, surge_len, skvaj, n_surge)
%GET_SURGE_PS —качок посто€нной составл€ющей
% null_len - определ€ет длину нулевого участка
% surge_len - длина скачка
% skvaj - коэффициент - часть null_len между скачками
% n_surge - количество скачков
    surge_ps = zeros(1, floor(null_len * skvaj));
    surge_ps_ind = zeros(0);
    n = n_surge;
    while n > 0
        n = n - 1;
        % 1
        surge_ps_ind = [surge_ps_ind, length(surge_ps) : 1 : (length(surge_ps) + surge_len)];
        surge_ps = [surge_ps, ones(1, surge_len)];
        % 0
        surge_ps = [surge_ps, zeros(1, floor(null_len * skvaj))]; %#ok<*AGROW>
    end
end
