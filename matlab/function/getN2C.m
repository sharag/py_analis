% Преобразовывает в формат N2С
% value - массив входных значений - только вектор, не матрица!
% kolRazr - количество разрядов числа (старший бит - прзнак знака)
function valueN2C = getN2C(value, kolRazr)
valueN2C = zeros(size(value));
for i=1:length(value)
    if bitget(value(i),kolRazr)
        valueN2C(i) = -((2^kolRazr - 1) - (value(i)-1));
    else
        valueN2C(i) = value(i);
    end
end
end