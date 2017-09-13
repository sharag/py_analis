function FGrafKorr(x, y, xz_1, xz_2, xz_3, z, xz1_1, xz1_2, xz1_3, z1, ...
    xz2_1, xz2_2, xz2_3, z2)
figure(1)
set(gcf, 'Name', 'Эталон соответствует по длине искомому фрагменту', ...
    'ToolBar', 'figure')

subplot(3, 1, 1)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz_2, z, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон смещен влево', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(3, 1, 2)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz_1, z, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон совмещен с искомым фрагментом', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(3, 1, 3)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz_3, z, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон смещен вправо', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

figure(2)
set(gcf, 'Name', 'Эталон шире искомого фрамента', ...
    'ToolBar', 'figure')

subplot(3, 1, 1)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz1_2, z1, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон смещен влево', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(3, 1, 2)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz1_1, z1, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон совмещен с искомым фрагментом', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(3, 1, 3)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz1_3, z1, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон смещен вправо', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

figure(3)
set(gcf, 'Name', 'Эталон уже искомого фрамента', ...
    'ToolBar', 'figure')

subplot(3, 1, 1)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz2_2, z2, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон смещен влево', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(3, 1, 2)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz2_1, z2, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон совмещен с искомым фрагментом', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);

subplot(3, 1, 3)
plot(x, y, 'LineWidth', 1)
hold on
plot(xz2_3, z2, 'LineWidth', 2, 'Color', 'Red')
hold off
title('Эталон смещен вправо', 'FontName', 'Times New Roman', 'FontSize', 10);
xlabel('Отсчеты', 'FontName', 'Times New Roman', 'FontSize', 10);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 10);
end