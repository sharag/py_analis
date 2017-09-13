%%ПО N при фиксированной M
clc
clear

N = 100 : 50 : 1000; % : 100 : 500;
Pp = [0.003 0.005 0.01 0.05]; %[0.01 0.05 0.1]; 
M = 1;
for p = 1:1:length(Pp)
    for n = 1 : 1 : length(N)
        for m = 1 : 1 : M
            % P(m, n + length(N)*(p - 1)) = (N(n)*Pp(p))^m*exp(-N(n)*Pp(p))/factorial(m); %по m
            P(p, n) = (N(n)*Pp(p))^m*exp(-N(n)*Pp(p))/factorial(m); % по n при фикс m
        end
    end
end
figure(2)
plot(N, P');
legend(num2str(Pp(1)), num2str(Pp(2)), num2str(Pp(3)), num2str(Pp(4)));

%% По N
clc
clear

N = 100 : 50 : 1000; % : 100 : 500;
Pp = [0.003 0.005 0.01 0.05]; %[0.01 0.05 0.1]; 
M = 3;
for p = 1:1:length(Pp)
    for n = 1 : 1 : length(N)
        for m = 1 : 1 : M
            % P(m, n + length(N)*(p - 1)) = (N(n)*Pp(p))^m*exp(-N(n)*Pp(p))/factorial(m); %по m
            P(p, n) = (N(n)*Pp(p))^m*exp(-Pp(p)/N(n))/factorial(m); % по n при фикс m
        end
    end
end
figure(2)
plot(N, P');
legend(num2str(Pp(1)), num2str(Pp(2)), num2str(Pp(3)), num2str(Pp(4)));