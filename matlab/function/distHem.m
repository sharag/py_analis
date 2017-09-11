% data1, data2 - могут быть массивами, wlen1, wlen1 - 
function [distH] = distHem(data1,wlen1,data2,wlen2)
n1=1;
dataA = 0;
for i = 1:length(data1)
    for j = 1:wlen1
        dataA(n1) = bitget(data1(i),j); %#ok<*AGROW>
        n1 = n1 + 1;
    end
end
n2=1;
dataB = 0;
for i = 1:length(data2)
    for j = 1:wlen2
        dataB(n2) = bitget(data2(i),j);
        n2 = n2 + 1;
    end
end
distH = sum(xor(dataA, dataB));
end