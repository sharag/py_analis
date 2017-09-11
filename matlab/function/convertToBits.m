function data = convertToBits(inData, numorder)
persentStep = fix(length(inData)/1000);
bitmask = zeros(1, numorder);
for i = 1:1:numorder
    bitmask(i) = 2^(numorder - i);
end
data = false(1, length(inData) * 8);
for i = 1:1:length(inData)
    for j = 1:1:8
        if (bitand(inData(i), bitmask(j)))
            data((i - 1) * 8 + j) = true;
        end
    end
    if rem(i,persentStep) == 0
        disp([num2str(i/10/persentStep), ' %']);
    end
end
end
