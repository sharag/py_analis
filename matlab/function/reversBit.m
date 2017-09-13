%% data = reversBit(inData, numorder)
function data = reversBit(inData, numorder)
data = zeros(size(inData));
persentStep = fix(length(inData)/1000);
for i = 1:1:length(inData)
    data(i) = revers(inData(i), numorder);
    if rem(i, persentStep) == 0
        disp([num2str(i/10/persentStep), ' %']);
    end
end
end