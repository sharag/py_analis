load histBitChange
histBitChange1 = zeros(size(histBitChange, 1), size(histBitChange, 2));
% ������������ �����������. ������� - ��� ���������� ��������� ������� 0
% ��� 1
for i = 1:size(histBitChange, 2)
    if histBitChange(i) > 2
        histBitChange1(i) = 0;
    else
        histBitChange1(i) = 1;
    end
end
% ���� ������ ������� ������� � ������ ������ �����
for i = 1:size(histBitChange1, 2) - 2
    if (histBitChange1(i) > 0) && (histBitChange1(i + 1) > 0) && (histBitChange1(i + 2) > 0)
        disp(['position: ', num2str(i)]);
        if fix((i - 1)/8) ~= fix(((i - 1) + 2) / 8)
            histBitChange1(i) = 0;
        end
    else
        histBitChange1(i) = 0;
    end
end

plot(histBitChange1);
ylim([-1 2]);
