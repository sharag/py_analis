function [rsample] = revers(sample, len)
rsample = 0;
for i = 1:len
    rsample = bitset(rsample,i,bitget(sample,(len-i+1)));
end
end