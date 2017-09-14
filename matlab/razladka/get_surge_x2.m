function [ surge_ps, surge_ps_ind ] = get_surge_x2( null_len, surge_len, skvaj, n_surge )
%GET_SURGE_X2 ��������������� ������ c �������� ���������� ��������
% null_len - ���������� ����� �������� �������
% surge_len - ����� ������
% skvaj - ����������� - ����� null_len ����� ��������
% n_surge - ���������� �������
    surge_ps = zeros(1, floor(null_len * skvaj));
    surge_ps_ind = zeros(0);
    n = n_surge;
    while n > 0
        n = n - 1;
        % 1
        surge_ps_ind = [surge_ps_ind, length(surge_ps) : 1 : (length(surge_ps) + surge_len)];
        surge_ps = [surge_ps, (((1 : 1 : (surge_len / 4)) / (surge_len / 4)) .^ 2) ./ 2 ];
        surge_ps = [surge_ps, (1 - (((1 : 1 : (surge_len / 4)) - surge_len / 4) / (surge_len / 4)) .^ 2) ./ 2 + 0.5];
        
        
        %surge = np.append(surge,(1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5 for x in range(surge_len // 4)])
        %surge = np.append(surge, [1 - (((x / (surge_len / 4)) ** 2) / 2) for x in range(surge_len // 4)])
        %surge = np.append(surge,[1 - ((1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5) for x in range(surge_len // 4)])
        
        
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
        
        surge_ps = [surge_ps, ((surge_len / 2) : -1 : 1) ./ (surge_len / 2)];
        % 0
        surge_ps = [surge_ps, zeros(1, floor(null_len * skvaj))]; %#ok<*AGROW>
    end


end

