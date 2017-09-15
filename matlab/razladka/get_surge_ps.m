function [s, sInd] = get_surge_ps(len0, lenS, skvaj, num_s)
%GET_SURGE_PS ������ ���������� ������������
% len0 - ���������� ����� �������� �������
% lenS - ����� ������
% skvaj - ����������� - ����� null_len ����� ��������
% num_s - ���������� �������
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
