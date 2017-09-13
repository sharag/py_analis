j=0;
x=-5:0.01:5;
n = -1:1:0;
for i = 1:length(n)
    for k = 1:length(x)
        y(k) = sqrt(2^j)*(sin(pi*((2^j)*x(k) - n(i)))/(pi*x(k)));
    end
    plot(x,y)
    hold on
    
end