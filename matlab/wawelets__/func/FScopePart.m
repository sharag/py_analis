function [beginPart, endPart] = FScopePart(beginPart, endPart)
prompt = {'������� ����� �������� ������ �������� ���������:', ...
    '������� ����� �������� ����� �������� ���������:'};
dlg_title = '���� ������ �������� ���������';
num_lines = 1;
def = {num2str(beginPart), num2str(endPart)};
answer = inputdlg(prompt ,dlg_title, num_lines, def);
beginPart = str2double(answer{1});
endPart = str2double(answer{2});
end