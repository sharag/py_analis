function FGrafTMP(TMPData, TMPAxeX, TMPName, Message)
figure;
set(gcf, 'Name', ['График ТМП: ' TMPName], ...
    'ToolBar', 'figure');
plot(TMPAxeX, TMPData, 'LineWidth', 2);
title(Message, 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('Значения', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
end