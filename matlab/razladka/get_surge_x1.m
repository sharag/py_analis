function [ s, sInd ] = get_surge_x1( len0, lenS, skvaj, numS )
%GET_SURGE_X1 ��������������� ������ c �������� ���������� ��������
% null_len - ���������� ����� �������� �������
% surge_len - ����� ������
% skvaj - ����������� - ����� null_len ����� ��������
% n_surge - ���������� �������
    s = zeros(1, floor(len0 * skvaj));
    sInd = zeros(0);
    n = numS;
    while n > 0
        n = n - 1;
        % 1
        sInd = [sInd, length(s) + 1 : 1 : (length(s) + lenS)];
        s = [s, (1 : 1 : floor(lenS / 2)) ./ floor(lenS / 2)];
        s = [s, (floor(lenS / 2) : -1 : 1) ./ floor(lenS / 2)];
        % 0
        s = [s, zeros(1, floor(len0 * skvaj))]; %#ok<*AGROW>
    end
end

