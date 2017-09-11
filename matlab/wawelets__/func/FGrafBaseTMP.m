function FGrafBaseTMP(baseTMPData, baseTMPFName)
figure(1);
set(gcf, 'Name', ['������ �������� ���: ' baseTMPFName], ...
    'ToolBar', 'figure');
plot(baseTMPData, 'LineWidth', 1);
title('���������� ������ �������� ������ � ����� �������� ���������', 'FontName', 'Times New Roman', 'FontSize', 12);
xlabel('��������', 'FontName', 'Times New Roman', 'FontSize', 12);
ylabel('���������', 'FontName', 'Times New Roman', 'FontSize', 12);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 12);
uicontrol('Position', [20 20 200 40], 'String', '����������', ...
              'Callback', 'uiresume(gcbf)');
uiwait(gcf);
close(figure(1));
end