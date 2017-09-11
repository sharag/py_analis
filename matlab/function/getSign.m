% ��������������� �� ������������ ������������� � ��������
% unsignValue - ������ ������� �������� - ������ ������, �� �������!
% kolRazr - ���������� �������� ����� (�������������� - ������� ��� - ������ �����)
function signValue = getSign(unsignValue, kolRazr)
signValue = zeros(1,length(unsignValue));
shift = 2^kolRazr;
for i=1:length(unsignValue)
    if unsignValue(i) > (shift/2)
        signValue(i) = unsignValue(i)-shift;
    else
        signValue(i) = unsignValue(i);
    end
end
end