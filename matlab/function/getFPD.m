% ������� �������� ����� �� 16-������ ���������� � 32-������ �����
function value = getFPD(exp,fraction)
    value = (2.^getN2C(exp,16)).*(getN2C(fraction,32)/231);
end