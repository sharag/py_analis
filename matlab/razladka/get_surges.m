function [surge_ps, surge_lin, surge_kvadr, surge_highcos] = get_surges(null_len, surge_len, skvaj, n_surge)
    % null_len - ���������� ����� �������� �������
    % surge_len - ����� ������
    % skvaj - ����������� - ����� null_len ����� ��������
    % n_surge - ���������� �������

    % ������ ���������� ������������
    surge_ps = zeros(1, floor(null_len * skvaj));
    surge_ps_ind = zeros(0);
    n = n_surge;
    while n > 0
        n = n - 1;
        % 1
        surge_ps_ind = [surge_ps_ind, length(surge_ps) : 1 : (length(surge_ps) + floor(null_len * skvaj))];
        surge_ps = [surge_ps, ones(1, surge_len)];
        % 0
        surge_ps = [surge_ps, zeros(1, floor(null_len * skvaj))];
    end
end



def get_lin(null_len, surge_len, skvaj, n_surge):
    """null_len - ���������� ����� �������� �������
    surge_len - ����� ������
    skvaj - ����������� - ����� null_len ����� ��������
    n_surge - ���������� �������"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge

    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, ([x / (surge_len / 2) for x in range(surge_len // 2)]))
        surge = np.append(surge, ([(1 - x / (surge_len / 2)) for x in range(surge_len // 2)]))
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes


def get_kvadr(null_len, surge_len, skvaj, n_surge):
    """null_len - ���������� ����� �������� �������
    surge_len - ����� ������
    skvaj - ����������� - ����� null_len ����� ��������
    n_surge - ���������� �������"""
    # 0
    surge = np.array([0] * int(null_len * skvaj))
    surge_indexes = np.array([])
    n = n_surge

    while n:
        n -= 1
        # 1
        surge_indexes = np.append(surge_indexes, [i for i in range(surge.size, surge.size + surge_len)])
        surge = np.append(surge, [((x / (surge_len / 4)) ** 2) / 2 for x in range(surge_len // 4)])
        surge = np.append(surge,
                          [(1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5 for x in range(surge_len // 4)])
        surge = np.append(surge, [1 - (((x / (surge_len / 4)) ** 2) / 2) for x in range(surge_len // 4)])
        surge = np.append(surge,
                          [1 - ((1 - ((x - surge_len / 4) / (surge_len / 4)) ** 2) / 2 + 0.5)
                           for x in range(surge_len // 4)])
        surge = np.append(surge, ([0] * int(null_len * skvaj)))
        # 0
        surge = np.append(surge, ([0] * int(null_len * skvaj)))

    return surge, surge_indexes


def get_high_cos(null_len, surge_len, skvaj, n_surge):
    """null_len - ���������� ����� �������� �������
    surge_len - ����� ������
    skvaj - ����������� - ����� null_len ����� ��������
    n_surge - ���������� �������"""
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