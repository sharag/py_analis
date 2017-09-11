%%ПО N при фиксированной M
clc
clear

N = 0 : 5 : 1000; % : 100 : 500;
Pp = [0.001 0.005 0.01 0.05 0.1];
for p = 1:1:length(Pp)
    for n = 1 : 1 : length(N)
        P(p, n) = (1 - exp(-N(n)*Pp(p)))*0.89; % по n при фикс m
    end
end
const08 = zeros(1, length(N));
const08 = const08 + 0.8;
figure(1)
plot(N, P', N, const08,'LineWidth', 2);
xlabel('N', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('P(N)', 'FontName', 'Times New Roman', 'FontSize', 14, 'Rotation', 	0, 'HorizontalAlignment', 'right');
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14, 'YLim', [0 1]);
legend(['q = ' num2str(Pp(1))], ['q = ' num2str(Pp(2))], ['q = ' num2str(Pp(3))], ['q = ' num2str(Pp(4))], ['q = ' num2str(Pp(5))]);
