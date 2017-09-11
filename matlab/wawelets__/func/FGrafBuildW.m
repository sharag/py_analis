function FGrafBuildW(WaweData, psi_WData, freqDiskrData)
x = 1/freqDiskrData:1/freqDiskrData:length(WaweData)/freqDiskrData;
figure;
set(gcf, 'Name', 'График построенного вейвлета', 'ToolBar', 'figure');
plot(x, psi_WData.*max(WaweData)./2, x, WaweData, 'LineWidth', 1);
title('Полученный базисный вейвлет', 'FontName', 'Times New Roman', 'FontSize', 12);
xlabel('Значения', 'FontName', 'Times New Roman', 'FontSize', 12);
ylabel('Амплитуда', 'FontName', 'Times New Roman', 'FontSize', 12);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 12);
end