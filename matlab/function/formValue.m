% formValue([1;255],[1;1],[8,8])
function value = formValue(values, begbits, bitlens)
value = 0;
nbit =1;
for i=1:length(values)
    for bnum = 0:(bitlens(i)-1)
        value = bitset(value, nbit, bitget(values(i), (begbits(i)+bnum)));
        nbit = nbit + 1;
    end
end
end