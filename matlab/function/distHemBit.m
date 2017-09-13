function distH = distHemBit(data1, data2)
distH = sum(xor(data1, data2));
end