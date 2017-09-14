function [ surge_ps, surge_ps_ind ] = get_surge_hcos( null_len, surge_len, skvaj, n_surge )
%GET_SURGE_HCOS Кратковременный скачок типа приподнятого косинуса
% null_len - определяет длину нулевого участка
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
        surge_ps = [surge_ps, (((1 : 1 : (surge_len / 4)) / (surge_len / 4)) .^ 2) ./ 2 ];
        surge_ps = [surge_ps, (1 - ((1 : 1 : (surge_len / 4)) / (surge_len / 4)) .^ 2) ./ 2 + 0.5];
        
        
        %surge = np.append(surge, [((x / (surge_len / 4)) ** 2) / 2 for x in range(surge_len // 4)])
        %surge = np.append(surge,(1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5 for x in range(surge_len // 4)])
        %surge = np.append(surge, [1 - (((x / (surge_len / 4)) ** 2) / 2) for x in range(surge_len // 4)])
        %surge = np.append(surge,[1 - ((1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5) for x in range(surge_len // 4)])
        
        
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
        
        surge_ps = [surge_ps, ((surge_len / 2) : -1 : 1) ./ (surge_len / 2)];
        % 0
        surge_ps = [surge_ps, zeros(1, floor(null_len * skvaj))]; %#ok<*AGROW>
    end



def get_high_cos(null_len, surge_len, skvaj, n_surge):
    """null_len - определяет длину нулевого участка
    surge_len - длина скачка
    skvaj - коэффициент - часть null_len между скачками
    n_surge - количество скачков"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge
    x_array = np.linspace(np.pi, 3 * np.pi, surge_len)
    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, [np.cos(x) + 1 for x in x_array])
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes
end
end

