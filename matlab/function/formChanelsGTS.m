function GTS = formChanelsGTS(dataSinhr, lenWord)
%lenWord = 8;
if rem(size(dataSinhr, 2), lenWord)
    disp('Неверные параметры');
    exit(0);
end
GTS = zeros(size(dataSinhr, 1), size(dataSinhr, 2)/lenWord);
persentStep = fix(size(dataSinhr, 1)/1000);
for i = 1:size(dataSinhr, 1)
    for j = 1:1:(size(dataSinhr, 2)/8)
        for nbit = 1:1:lenWord
            GTS(i, j) = bitset(GTS(i, j), (lenWord + 1 - nbit), dataSinhr(i, (j-1)*lenWord + nbit));
        end
    end
    if rem(i,persentStep) == 0
        disp([num2str(i/10/persentStep), ' %']);
    end
end
end