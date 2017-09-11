function FGrafBaseTMP(baseTMPData, baseTMPFName)
figure(1);
set(gcf, 'Name', ['График базового ТМП: ' baseTMPFName], ...
    'ToolBar', 'figure');
plot(baseTMPData, 'LineWidth', 1);
title('Определите номера значений начала и конца искомого интервала', 'FontName', 'Times New Roman', 'FontSize', 12);
xlabel('Значения', 'FontName', 'Times New Roman', 'FontSize', 12);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 12);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 12);
uicontrol('Position', [20 20 200 40], 'String', 'Продолжить', ...
              'Callback', 'uiresume(gcbf)');
uiwait(gcf);
close(figure(1));
end