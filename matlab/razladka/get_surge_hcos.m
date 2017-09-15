function [ s, sInd ] = get_surge_hcos( len0, lenS, skvaj, num_s )
%GET_SURGE_HCOS ��������������� ������ ���� ������������ ��������
% null_len - ���������� ����� �������� �������
% surge_len - ����� ������
% skvaj - ����������� - ����� null_len ����� ��������
% n_surge - ���������� �������
    s = zeros(1, floor(len0 * skvaj));
    sInd = zeros(0);
    n = num_s;
    arg = (pi : (2 * pi) / (lenS - 1) : 3 * pi);
    while n > 0
        n = n - 1;
        % 1
        sInd = [sInd, length(s) + 1 : 1 : (length(s) + lenS)];
        s = [s, cos(arg) + 1];
        % 0
        s = [s, zeros(1, floor(len0 * skvaj))]; %#ok<*AGROW>
    end
end

