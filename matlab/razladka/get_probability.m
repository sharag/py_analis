function [ prob ] = get_probability( s, winBef, winAft )
%GET_PROBABILITY ������� ���������� ��������� �������������
% s - ������� ������, ��� list
% winBef - ����� ���� �� ������
% winAft - ����� ���� ����� ������

% ������������ ������� ��� �������� �������� ��������� ������������� ����������� ����
prob = zeros(1, length(s) - winBef - winAft);
for i = 1 : 1 : length(s) - winBef - winAft
    % �������������� �������� ���� �� ������
    meanBef = mean(s(i : i + winBef));
    % �������������� �������� ���� ����� ������
    meanAft = mean(s(i + winBef : i + winBef + winAft));
    % ��������� ����� ����
    varAll = var(s(i : i + winBef + winAft));
    if varAll == 0
        varAll = 0.000000001;
    end
    % ������� ����� ��� ��������� �������������
    summ = 0;
    for j = 1 : 1 : winAft
        summ = summ + ...
            (s(i + winBef + j) - meanBef - (meanAft - meanBef) / 2);
    end
    % ������ ��������� �������������
    prob(i) = (meanAft - meanBef) * summ / varAll;
end

end

