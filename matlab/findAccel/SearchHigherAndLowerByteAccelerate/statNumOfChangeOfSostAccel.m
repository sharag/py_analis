% clc;
% clear;
% 
% %���������
% decVal = 40;%��������� (1/40)
% fqFrAcclrt = 400;%������� ���������� �������� � �������
% sostNum = 0;%���������� ������������ ���������
% %������ ������������������: ������ - ���, ������� - �����
% timeStep = [625 1335 1762; 652 1345 1763; 637 1319 1738];
% 
% %������ ������
% %1-� ���
% [FNameDataA0_1, PathFNameDataA0_1] = uigetfile({'*.Ai0', ...
%     '���� ������������ ��������� A0'}, ...
%     '�������� ���� ������������ ��������� A0',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA0_1, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA0_1, FNameDataA0_1), '.']);
% end
% FIDDataA0_1 = fopen(fullfile(PathFNameDataA0_1, FNameDataA0_1), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_1(sostNum, :) = fread(FIDDataA0_1, 'int16');
% fclose(FIDDataA0_1);
% 
% [FNameDataA1_1, PathFNameDataA1_1] = uigetfile({'*.Ai1', ...
%     '���� ������������ ��������� A1'}, ...
%     '�������� ���� ������������ ��������� A1',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA1_1, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA1_1, FNameDataA1_1), '.']);
% end
% FIDDataA1_1 = fopen(fullfile(PathFNameDataA1_1, FNameDataA1_1), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_1(sostNum, :) = fread(FIDDataA1_1, 'int16');
% fclose(FIDDataA1_1);
% 
% [FNameDataA2_1, PathFNameDataA2_1] = uigetfile({'*.Ai2', ...
%     '���� ������������ ��������� A2'}, ...
%     '�������� ���� ������������ ��������� A2',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA2_1, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA2_1, FNameDataA2_1), '.']);
% end
% FIDDataA2_1 = fopen(fullfile(PathFNameDataA2_1, FNameDataA2_1), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_1(sostNum, :) = fread(FIDDataA2_1, 'int16');
% fclose(FIDDataA2_1);
% 
% %2-� ���
% [FNameDataA0_2, PathFNameDataA0_2] = uigetfile({'*.Ai0', ...
%     '���� ������������ ��������� A0'}, ...
%     '�������� ���� ������������ ��������� A0',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA0_2, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA0_2, FNameDataA0_2), '.']);
% end
% FIDDataA0_2 = fopen(fullfile(PathFNameDataA0_2, FNameDataA0_2), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_2(sostNum - 3, :) = fread(FIDDataA0_2, 'int16');
% fclose(FIDDataA0_2);
% 
% [FNameDataA1_2, PathFNameDataA1_2] = uigetfile({'*.Ai1', ...
%     '���� ������������ ��������� A1'}, ...
%     '�������� ���� ������������ ��������� A1',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA1_2, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA1_2, FNameDataA1_2), '.']);
% end
% FIDDataA1_2 = fopen(fullfile(PathFNameDataA1_2, FNameDataA1_2), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_2(sostNum - 3, :) = fread(FIDDataA1_2, 'int16');
% fclose(FIDDataA1_2);
% 
% [FNameDataA2_2, PathFNameDataA2_2] = uigetfile({'*.Ai2', ...
%     '���� ������������ ��������� A2'}, ...
%     '�������� ���� ������������ ��������� A2',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA2_2, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA2_2, FNameDataA2_2), '.']);
% end
% FIDDataA2_2 = fopen(fullfile(PathFNameDataA2_2, FNameDataA2_2), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_2(sostNum - 3, :) = fread(FIDDataA2_2, 'int16');
% fclose(FIDDataA2_2);
% 
% %3-� ���
% [FNameDataA0_3, PathFNameDataA0_3] = uigetfile({'*.Ai0', ...
%     '���� ������������ ��������� A0'}, ...
%     '�������� ���� ������������ ��������� A0',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA0_3, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA0_3, FNameDataA0_3), '.']);
% end
% FIDDataA0_3 = fopen(fullfile(PathFNameDataA0_3, FNameDataA0_3), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_3(sostNum - 6, :) = fread(FIDDataA0_3, 'int16');
% fclose(FIDDataA0_3);
% 
% [FNameDataA1_3, PathFNameDataA1_3] = uigetfile({'*.Ai1', ...
%     '���� ������������ ��������� A1'}, ...
%     '�������� ���� ������������ ��������� A1',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA1_3, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA1_3, FNameDataA1_3), '.']);
% end
% FIDDataA1_3 = fopen(fullfile(PathFNameDataA1_3, FNameDataA1_3), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_3(sostNum - 6, :) = fread(FIDDataA1_3, 'int16');
% fclose(FIDDataA1_3);
% 
% [FNameDataA2_3, PathFNameDataA2_3] = uigetfile({'*.Ai2', ...
%     '���� ������������ ��������� A2'}, ...
%     '�������� ���� ������������ ��������� A2',...
%     'd:\work\telemetry\trident\');
% if isequal(FNameDataA2_3, 0)
%    disp('����� ����� �������.');
%    break;
% else
%    disp(['������ ����: ', fullfile(PathFNameDataA2_3, FNameDataA2_3), '.']);
% end
% FIDDataA2_3 = fopen(fullfile(PathFNameDataA2_3, FNameDataA2_3), 'r');
% sostNum = sostNum + 1;
% DataAcclrt_3(sostNum - 6, :) = fread(FIDDataA2_3, 'int16');
% fclose(FIDDataA2_3);
% clear FIDDataA0_1 FIDDataA1_1 FIDDataA2_1 
% clear FNameDataA0_1 FNameDataA1_1 FNameDataA2_1
% clear PathFNameDataA1_1 PathFNameDataA2_1
% clear FIDDataA0_2 FIDDataA1_2 FIDDataA2_2 
% clear FNameDataA0_2 FNameDataA1_2 FNameDataA2_2
% clear PathFNameDataA0_2 PathFNameDataA1_2 PathFNameDataA2_2
% clear FIDDataA0_3 FIDDataA1_3 FIDDataA2_3 
% clear FNameDataA0_3 FNameDataA1_3 FNameDataA2_3
% clear PathFNameDataA0_3 PathFNameDataA1_3 PathFNameDataA2_3 sostNum
% 
% %������������ ������������ ��������� - 1/40, ��� ��� ������ ���� 40 ���������� ��������
% DataAcclrtDec_1 = zeros(3, floor(size(DataAcclrt_1, 2)/decVal));
% DataAcclrtDec_2 = zeros(3, floor(size(DataAcclrt_2, 2)/decVal));
% DataAcclrtDec_3 = zeros(3, floor(size(DataAcclrt_3, 2)/decVal));
% ii = 1;
% for i=1:decVal:(length(DataAcclrt_1) - decVal + 1)
%     DataAcclrtDec_1(:, ii) = DataAcclrt_1(:, i); %#ok<SAGROW>
%     ii = ii + 1;
% end
% ii = 1;
% for i=1:decVal:(length(DataAcclrt_2) - decVal + 1)
%     DataAcclrtDec_2(:, ii) = DataAcclrt_2(:, i); %#ok<SAGROW>
%     ii = ii + 1;
% end
% ii = 1;
% for i=1:decVal:(length(DataAcclrt_3) - decVal + 1)
%     DataAcclrtDec_3(:, ii) = DataAcclrt_3(:, i); %#ok<SAGROW>
%     ii = ii + 1;
% end
% clear i ii DataAcclrt_1 DataAcclrt_2 DataAcclrt_3
% fqFrAcclrt = fqFrAcclrt/decVal;%������� ���������� �������� � �������
% stepTimeAcclrt = 1/fqFrAcclrt;%��� ��������� ����� � ������ ���������
% clear fqFrAcclrt
% disp('��������� ������������ ��������� �����������.');

%������������ ������ ��������� � ��������� ������ ������������������
accelPartsLow_1 = zeros(3, size(DataAcclrtDec_1, 2) - timeStep(1, 3) + 1);
accelPartsHight_1 = zeros(3, size(DataAcclrtDec_1, 2) - timeStep(1, 3) + 1);
accelPartsHight_1(1, :) = fix(DataAcclrtDec_1(1, timeStep(1, 3):end)./256);
accelPartsHight_1(2, :) = fix(DataAcclrtDec_1(2, timeStep(1, 3):end)./256);
accelPartsHight_1(3, :) = fix(DataAcclrtDec_1(3, timeStep(1, 3):end)./256);
accelPartsLow_1(1, :) = mod(DataAcclrtDec_1(1, timeStep(1, 3):end), 256);
accelPartsLow_1(2, :) = mod(DataAcclrtDec_1(2, timeStep(1, 3):end), 256);
accelPartsLow_1(3, :) = mod(DataAcclrtDec_1(3, timeStep(1, 3):end), 256);

accelPartsLow_2 = zeros(3, size(DataAcclrtDec_2, 2) - timeStep(2, 3) + 1);
accelPartsHight_2 = zeros(3, size(DataAcclrtDec_2, 2) - timeStep(2, 3) + 1);
accelPartsHight_2(1, :) = fix(DataAcclrtDec_2(1, timeStep(2, 3):end)./256);
accelPartsHight_2(2, :) = fix(DataAcclrtDec_2(2, timeStep(2, 3):end)./256);
accelPartsHight_2(3, :) = fix(DataAcclrtDec_2(3, timeStep(2, 3):end)./256);
accelPartsLow_2(1, :) = mod(DataAcclrtDec_2(1, timeStep(2, 3):end), 256);
accelPartsLow_2(2, :) = mod(DataAcclrtDec_2(2, timeStep(2, 3):end), 256);
accelPartsLow_2(3, :) = mod(DataAcclrtDec_2(3, timeStep(2, 3):end), 256);

accelPartsLow_3 = zeros(3, size(DataAcclrtDec_3, 2) - timeStep(3, 3) + 1);
accelPartsHight_3 = zeros(3, size(DataAcclrtDec_3, 2) - timeStep(3, 3) + 1);
accelPartsHight_3(1, :) = fix(DataAcclrtDec_3(1, timeStep(3, 3):end)./256);
accelPartsHight_3(2, :) = fix(DataAcclrtDec_3(2, timeStep(3, 3):end)./256);
accelPartsHight_3(3, :) = fix(DataAcclrtDec_3(3, timeStep(3, 3):end)./256);
accelPartsLow_3(1, :) = mod(DataAcclrtDec_3(1, timeStep(3, 3):end), 256);
accelPartsLow_3(2, :) = mod(DataAcclrtDec_3(2, timeStep(3, 3):end), 256);
accelPartsLow_3(3, :) = mod(DataAcclrtDec_3(3, timeStep(3, 3):end), 256);

% %������������ ������ ��������� � ������� ������ ������������������
% accelPartsLow_1 = zeros(3, timeStep(1, 3) - timeStep(1, 2) + 1);
% accelPartsHight_1 = zeros(3, timeStep(1, 3) - timeStep(1, 2) + 1);
% accelPartsHight_1(1, :) = fix(DataAcclrtDec_1(1, timeStep(1, 2):timeStep(1, 3))./256);
% accelPartsHight_1(2, :) = fix(DataAcclrtDec_1(2, timeStep(1, 2):timeStep(1, 3))./256);
% accelPartsHight_1(3, :) = fix(DataAcclrtDec_1(3, timeStep(1, 2):timeStep(1, 3))./256);
% accelPartsLow_1(1, :) = mod(DataAcclrtDec_1(1, timeStep(1, 2):timeStep(1, 3)), 256);
% accelPartsLow_1(2, :) = mod(DataAcclrtDec_1(2, timeStep(1, 2):timeStep(1, 3)), 256);
% accelPartsLow_1(3, :) = mod(DataAcclrtDec_1(3, timeStep(1, 2):timeStep(1, 3)), 256);
% 
% accelPartsLow_2 = zeros(3, timeStep(2, 3) - timeStep(2, 2) + 1);
% accelPartsHight_2 = zeros(3, timeStep(2, 3) - timeStep(2, 2) + 1);
% accelPartsHight_2(1, :) = fix(DataAcclrtDec_2(1, timeStep(2, 2):timeStep(2, 3))./256);
% accelPartsHight_2(2, :) = fix(DataAcclrtDec_2(2, timeStep(2, 2):timeStep(2, 3))./256);
% accelPartsHight_2(3, :) = fix(DataAcclrtDec_2(3, timeStep(2, 2):timeStep(2, 3))./256);
% accelPartsLow_2(1, :) = mod(DataAcclrtDec_2(1, timeStep(2, 2):timeStep(2, 3)), 256);
% accelPartsLow_2(2, :) = mod(DataAcclrtDec_2(2, timeStep(2, 2):timeStep(2, 3)), 256);
% accelPartsLow_2(3, :) = mod(DataAcclrtDec_2(3, timeStep(2, 2):timeStep(2, 3)), 256);
% 
% accelPartsLow_3 = zeros(3, timeStep(3, 3) - timeStep(3, 2) + 1);
% accelPartsHight_3 = zeros(3, timeStep(3, 3) - timeStep(3, 2) + 1);
% accelPartsHight_3(1, :) = fix(DataAcclrtDec_3(1, timeStep(3, 2):timeStep(3, 3))./256);
% accelPartsHight_3(2, :) = fix(DataAcclrtDec_3(2, timeStep(3, 2):timeStep(3, 3))./256);
% accelPartsHight_3(3, :) = fix(DataAcclrtDec_3(3, timeStep(3, 2):timeStep(3, 3))./256);
% accelPartsLow_3(1, :) = mod(DataAcclrtDec_3(1, timeStep(3, 2):timeStep(3, 3)), 256);
% accelPartsLow_3(2, :) = mod(DataAcclrtDec_3(2, timeStep(3, 2):timeStep(3, 3)), 256);
% accelPartsLow_3(3, :) = mod(DataAcclrtDec_3(3, timeStep(3, 2):timeStep(3, 3)), 256);

% %������������ ������ ��������� �� ������ ������ ������������������
% accelPartsLow_1 = zeros(3, timeStep(1, 2) - timeStep(1, 1) + 1);
% accelPartsHight_1 = zeros(3, timeStep(1, 2) - timeStep(1, 1) + 1);
% accelPartsHight_1(1, :) = fix(DataAcclrtDec_1(1, timeStep(1, 1):timeStep(1, 2))./256);
% accelPartsHight_1(2, :) = fix(DataAcclrtDec_1(2, timeStep(1, 1):timeStep(1, 2))./256);
% accelPartsHight_1(3, :) = fix(DataAcclrtDec_1(3, timeStep(1, 1):timeStep(1, 2))./256);
% accelPartsLow_1(1, :) = mod(DataAcclrtDec_1(1, timeStep(1, 1):timeStep(1, 2)), 256);
% accelPartsLow_1(2, :) = mod(DataAcclrtDec_1(2, timeStep(1, 1):timeStep(1, 2)), 256);
% accelPartsLow_1(3, :) = mod(DataAcclrtDec_1(3, timeStep(1, 1):timeStep(1, 2)), 256);
% 
% accelPartsLow_2 = zeros(3, timeStep(2, 2) - timeStep(2, 1) + 1);
% accelPartsHight_2 = zeros(3, timeStep(2, 2) - timeStep(2, 1) + 1);
% accelPartsHight_2(1, :) = fix(DataAcclrtDec_2(1, timeStep(2, 1):timeStep(2, 2))./256);
% accelPartsHight_2(2, :) = fix(DataAcclrtDec_2(2, timeStep(2, 1):timeStep(2, 2))./256);
% accelPartsHight_2(3, :) = fix(DataAcclrtDec_2(3, timeStep(2, 1):timeStep(2, 2))./256);
% accelPartsLow_2(1, :) = mod(DataAcclrtDec_2(1, timeStep(2, 1):timeStep(2, 2)), 256);
% accelPartsLow_2(2, :) = mod(DataAcclrtDec_2(2, timeStep(2, 1):timeStep(2, 2)), 256);
% accelPartsLow_2(3, :) = mod(DataAcclrtDec_2(3, timeStep(2, 1):timeStep(2, 2)), 256);
% 
% accelPartsLow_3 = zeros(3, timeStep(3, 2) - timeStep(3, 1) + 1);
% accelPartsHight_3 = zeros(3, timeStep(3, 2) - timeStep(3, 1) + 1);
% accelPartsHight_3(1, :) = fix(DataAcclrtDec_3(1, timeStep(3, 1):timeStep(3, 2))./256);
% accelPartsHight_3(2, :) = fix(DataAcclrtDec_3(2, timeStep(3, 1):timeStep(3, 2))./256);
% accelPartsHight_3(3, :) = fix(DataAcclrtDec_3(3, timeStep(3, 1):timeStep(3, 2))./256);
% accelPartsLow_3(1, :) = mod(DataAcclrtDec_3(1, timeStep(3, 1):timeStep(3, 2)), 256);
% accelPartsLow_3(2, :) = mod(DataAcclrtDec_3(2, timeStep(3, 1):timeStep(3, 2)), 256);
% accelPartsLow_3(3, :) = mod(DataAcclrtDec_3(3, timeStep(3, 1):timeStep(3, 2)), 256);

% %������������ ������ ��������� � ������ ������ ������������������
% accelPartsLow_1 = zeros(3, timeStep(1, 1));
% accelPartsHight_1 = zeros(3, timeStep(1, 1));
% accelPartsHight_1(1, :) = fix(DataAcclrtDec_1(1, 1:timeStep(1, 1))./256);
% accelPartsHight_1(2, :) = fix(DataAcclrtDec_1(2, 1:timeStep(1, 1))./256);
% accelPartsHight_1(3, :) = fix(DataAcclrtDec_1(3, 1:timeStep(1, 1))./256);
% accelPartsLow_1(1, :) = mod(DataAcclrtDec_1(1, 1:timeStep(1, 1)), 256);
% accelPartsLow_1(2, :) = mod(DataAcclrtDec_1(2, 1:timeStep(1, 1)), 256);
% accelPartsLow_1(3, :) = mod(DataAcclrtDec_1(3, 1:timeStep(1, 1)), 256);
% 
% accelPartsLow_2 = zeros(3, timeStep(2, 1));
% accelPartsHight_2 = zeros(3, timeStep(2, 1));
% accelPartsHight_2(1, :) = fix(DataAcclrtDec_2(1, 1:timeStep(2, 1))./256);
% accelPartsHight_2(2, :) = fix(DataAcclrtDec_2(2, 1:timeStep(2, 1))./256);
% accelPartsHight_2(3, :) = fix(DataAcclrtDec_2(3, 1:timeStep(2, 1))./256);
% accelPartsLow_2(1, :) = mod(DataAcclrtDec_2(1, 1:timeStep(2, 1)), 256);
% accelPartsLow_2(2, :) = mod(DataAcclrtDec_2(2, 1:timeStep(2, 1)), 256);
% accelPartsLow_2(3, :) = mod(DataAcclrtDec_2(3, 1:timeStep(2, 1)), 256);
% 
% accelPartsLow_3 = zeros(3, timeStep(3, 1));
% accelPartsHight_3 = zeros(3, timeStep(3, 1));
% accelPartsHight_3(1, :) = fix(DataAcclrtDec_3(1, 1:timeStep(3, 1))./256);
% accelPartsHight_3(2, :) = fix(DataAcclrtDec_3(2, 1:timeStep(3, 1))./256);
% accelPartsHight_3(3, :) = fix(DataAcclrtDec_3(3, 1:timeStep(3, 1))./256);
% accelPartsLow_3(1, :) = mod(DataAcclrtDec_3(1, 1:timeStep(3, 1)), 256);
% accelPartsLow_3(2, :) = mod(DataAcclrtDec_3(2, 1:timeStep(3, 1)), 256);
% accelPartsLow_3(3, :) = mod(DataAcclrtDec_3(3, 1:timeStep(3, 1)), 256);

% %������������ ������ ��������� ��� ������� ���
% accelPartsLow_1 = zeros(3, size(DataAcclrtDec_1, 2));
% accelPartsHight_1 = zeros(3, size(DataAcclrtDec_1, 2));
% accelPartsHight_1(1, :) = fix(DataAcclrtDec_1(1, :)./256);
% accelPartsHight_1(2, :) = fix(DataAcclrtDec_1(2, :)./256);
% accelPartsHight_1(3, :) = fix(DataAcclrtDec_1(3, :)./256);
% accelPartsLow_1(1, :) = mod(DataAcclrtDec_1(1, :), 256);
% accelPartsLow_1(2, :) = mod(DataAcclrtDec_1(2, :), 256);
% accelPartsLow_1(3, :) = mod(DataAcclrtDec_1(3, :), 256);
% 
% accelPartsLow_2 = zeros(3, size(DataAcclrtDec_2, 2));
% accelPartsHight_2 = zeros(3, size(DataAcclrtDec_2, 2));
% accelPartsHight_2(1, :) = fix(DataAcclrtDec_2(1, :)./256);
% accelPartsHight_2(2, :) = fix(DataAcclrtDec_2(2, :)./256);
% accelPartsHight_2(3, :) = fix(DataAcclrtDec_2(3, :)./256);
% accelPartsLow_2(1, :) = mod(DataAcclrtDec_2(1, :), 256);
% accelPartsLow_2(2, :) = mod(DataAcclrtDec_2(2, :), 256);
% accelPartsLow_2(3, :) = mod(DataAcclrtDec_2(3, :), 256);
% 
% accelPartsLow_3 = zeros(3, size(DataAcclrtDec_3, 2));
% accelPartsHight_3 = zeros(3, size(DataAcclrtDec_3, 2));
% accelPartsHight_3(1, :) = fix(DataAcclrtDec_3(1, :)./256);
% accelPartsHight_3(2, :) = fix(DataAcclrtDec_3(2, :)./256);
% accelPartsHight_3(3, :) = fix(DataAcclrtDec_3(3, :)./256);
% accelPartsLow_3(1, :) = mod(DataAcclrtDec_3(1, :), 256);
% accelPartsLow_3(2, :) = mod(DataAcclrtDec_3(2, :), 256);
% accelPartsLow_3(3, :) = mod(DataAcclrtDec_3(3, :), 256);
% 
% disp('������������ ��������� ��������� �� �����.');

% ���������� ��� ������� ��� 
statNumOfChangeLow_1 = zeros(3, size(accelPartsLow_1, 2));
statNumOfChangeHi_1 = zeros(3, size(accelPartsHight_1, 2));
statNumOfChangeLow_2 = zeros(3, size(accelPartsLow_2, 2));
statNumOfChangeHi_2 = zeros(3, size(accelPartsHight_2, 2));
statNumOfChangeLow_3 = zeros(3, size(accelPartsLow_3, 2));
statNumOfChangeHi_3 = zeros(3, size(accelPartsHight_3, 2));
for i=1:1:3%���������� ������������
    oldValLow = 0;
    oldValLowIndex = 0;
    oldValHi = 0;
    oldValHiIndex = 0;
    for j = 1:1:size(accelPartsLow_1, 2)
        if oldValLow ~= accelPartsLow_1(i, j)
            statNumOfChangeLow_1(i, j - oldValLowIndex) = statNumOfChangeLow_1(i, j - oldValLowIndex) + 1;
            oldValLow = accelPartsLow_1(i, j);
            oldValLowIndex = j;
        end
        if oldValHi ~= accelPartsHight_1(i, j)
            statNumOfChangeHi_1(i, j - oldValHiIndex) = statNumOfChangeHi_1(i, j - oldValHiIndex) + 1;
            oldValHi = accelPartsHight_1(i, j);
            oldValHiIndex = j;
        end
    end
    oldValLow = 0;
    oldValLowIndex = 0;
    oldValHi = 0;
    oldValHiIndex = 0;
    for j = 1:1:size(accelPartsLow_2, 2)
        if oldValLow ~= accelPartsLow_2(i, j)
            statNumOfChangeLow_2(i, j - oldValLowIndex) = statNumOfChangeLow_2(i, j - oldValLowIndex) + 1;
            oldValLow = accelPartsLow_2(i, j);
            oldValLowIndex = j;
        end
        if oldValHi ~= accelPartsHight_2(i, j)
            statNumOfChangeHi_2(i, j - oldValHiIndex) = statNumOfChangeHi_2(i, j - oldValHiIndex) + 1;
            oldValHi = accelPartsHight_2(i, j);
            oldValHiIndex = j;
        end
    end
    oldValLow = 0;
    oldValLowIndex = 0;
    oldValHi = 0;
    oldValHiIndex = 0;
    for j = 1:1:size(accelPartsLow_3, 2)
        if oldValLow ~= accelPartsLow_3(i, j)
            statNumOfChangeLow_3(i, j - oldValLowIndex) = statNumOfChangeLow_3(i, j - oldValLowIndex) + 1;
            oldValLow = accelPartsLow_3(i, j);
            oldValLowIndex = j;
        end
        if oldValHi ~= accelPartsHight_3(i, j)
            statNumOfChangeHi_3(i, j - oldValHiIndex) = statNumOfChangeHi_3(i, j - oldValHiIndex) + 1;
            oldValHi = accelPartsHight_3(i, j);
            oldValHiIndex = j;
        end
    end
end
clear oldValLow oldValLowIndex oldValHi oldValHiIndex

%��������� �����������
%����� ����� ������� ������������������
lengthMax = 0;
for i = 1:1:3
    for j = 1:1:size(accelPartsLow_1, 2)
        if statNumOfChangeLow_1(i, j) ~= 0 && j > lengthMax
            lengthMax = lengthMax + 1;
        end
        if statNumOfChangeHi_1(i, j) ~= 0 && j > lengthMax
            lengthMax = lengthMax + 1;
        end
    end
    for j = 1:1:size(accelPartsLow_2, 2)
        if statNumOfChangeLow_2(i, j) ~= 0 && j > lengthMax
            lengthMax = lengthMax + 1;
        end
        if statNumOfChangeHi_2(i, j) ~= 0 && j > lengthMax
            lengthMax = lengthMax + 1;
        end
    end
    for j = 1:1:size(accelPartsLow_3, 2)
        if statNumOfChangeLow_3(i, j) ~= 0 && j > lengthMax
            lengthMax = lengthMax + 1;
        end
        if statNumOfChangeHi_3(i, j) ~= 0 && j > lengthMax
            lengthMax = lengthMax + 1;
        end
    end
end
%�������� ������ ���������
statNumOfChangeLow_1(:, (lengthMax + 1):end) = [];
statNumOfChangeHi_1(:, (lengthMax + 1):end) = [];
statNumOfChangeLow_2(:, (lengthMax + 1):end) = [];
statNumOfChangeHi_2(:, (lengthMax + 1):end) = [];
statNumOfChangeLow_3(:, (lengthMax + 1):end) = [];
statNumOfChangeHi_3(:, (lengthMax + 1):end) = [];

disp('���������� ��������� ����������.');

%������ - ������������, ������� - ��������, ��� Z - ���
statNumOfChangeLow = zeros(3, lengthMax, 3);
statNumOfChangeHi = zeros(3, lengthMax, 3);
statNumOfChangeLow(:, :, 1) = statNumOfChangeLow_1;
statNumOfChangeLow(:, :, 2) = statNumOfChangeLow_2;
statNumOfChangeLow(:, :, 3) = statNumOfChangeLow_3;
statNumOfChangeHi(:, :, 1) = statNumOfChangeHi_1;
statNumOfChangeHi(:, :, 2) = statNumOfChangeHi_2;
statNumOfChangeHi(:, :, 3) = statNumOfChangeHi_3;

clear statNumOfChangeLow_1 statNumOfChangeLow_2 statNumOfChangeLow_3
clear statNumOfChangeHi_1 statNumOfChangeHi_2 statNumOfChangeHi_3

axeTimeStat = (1:1:size(statNumOfChangeLow, 2));
%������� �� ������������
figure(1);
bar(axeTimeStat, statNumOfChangeLow(:, :, 1)');
title('1998 ���, ������� �������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1 ������������', '2 ������������', '3 ������������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(2);
bar(axeTimeStat, statNumOfChangeHi(:, :, 1)');
title('1998 ���, ������� �������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1 ������������', '2 ������������', '3 ������������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(3);
bar(axeTimeStat, statNumOfChangeLow(:, :, 2)');
title('1999 ���, ������� �������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1 ������������', '2 ������������', '3 ������������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(4);
bar(axeTimeStat, statNumOfChangeHi(:, :, 2)');
title('1999 ���, ������� �������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1 ������������', '2 ������������', '3 ������������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(5);
bar(axeTimeStat, statNumOfChangeLow(:, :, 3)');
title('2000 ���, ������� �������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1 ������������', '2 ������������', '3 ������������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(6);
bar(axeTimeStat, statNumOfChangeHi(:, :, 3)');
title('2000 ���, ������� �������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1 ������������', '2 ������������', '3 ������������');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

temp = zeros(3, size(statNumOfChangeLow, 2));
%������� �� �����
figure(7);
temp(1,:) = statNumOfChangeLow(1, :, 1);
temp(2,:) = statNumOfChangeLow(1, :, 2);
temp(3,:) = statNumOfChangeLow(1, :, 3);
bar(axeTimeStat, temp');
title('������� �������, 1 ������������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1998 ���', '1999 ���', '2000 ���');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(8);
temp(1,:) = statNumOfChangeLow(2, :, 1);
temp(2,:) = statNumOfChangeLow(2, :, 2);
temp(3,:) = statNumOfChangeLow(2, :, 3);
bar(axeTimeStat, temp');
title('������� �������, 2 ������������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1998 ���', '1999 ���', '2000 ���');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(9);
temp(1,:) = statNumOfChangeLow(3, :, 1);
temp(2,:) = statNumOfChangeLow(3, :, 2);
temp(3,:) = statNumOfChangeLow(3, :, 3);
bar(axeTimeStat, temp');
title('������� �������, 3 ������������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1998 ���', '1999 ���', '2000 ���');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(10);
temp(1,:) = statNumOfChangeHi(1, :, 1);
temp(2,:) = statNumOfChangeHi(1, :, 2);
temp(3,:) = statNumOfChangeHi(1, :, 3);
bar(axeTimeStat, temp');
title('������� �������, 1 ������������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1998 ���', '1999 ���', '2000 ���');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(11);
temp(1,:) = statNumOfChangeHi(2, :, 1);
temp(2,:) = statNumOfChangeHi(2, :, 2);
temp(3,:) = statNumOfChangeHi(2, :, 3);
bar(axeTimeStat, temp');
title('������� �������, 2 ������������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1998 ���', '1999 ���', '2000 ���');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

figure(12);
temp(1,:) = statNumOfChangeHi(3, :, 1);
temp(2,:) = statNumOfChangeHi(3, :, 2);
temp(3,:) = statNumOfChangeHi(3, :, 3);
bar(axeTimeStat, temp');
title('������� �������, 3 ������������', 'FontName', 'Times New Roman', 'FontSize', 14);
xlabel('������ ��������� ���������', 'FontName', 'Times New Roman', 'FontSize', 14);
ylabel('���������� ��������� � �������� ����������', 'FontName', 'Times New Roman', 'FontSize', 14);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
hlegeng = legend('1998 ���', '1999 ���', '2000 ���');
set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);

clear temp hlegeng

%������ ����������
sumHiSost(1, :) = [0 1998 1999 2000];%������ - ������������, ������� - ����
sumHiSost(2:4, 1) = 1:3;
sumHiSost(2:4, 2) = sum(statNumOfChangeHi(:, :, 1)');%98 ���
sumHiSost(2:4, 3) = sum(statNumOfChangeHi(:, :, 2)');%99 ���
sumHiSost(2:4, 4) = sum(statNumOfChangeHi(:, :, 3)');%00 ���
sumLowSost(1, :) = [0 1998 1999 2000];%������ - ������������, ������� - ����
sumLowSost(2:4, 1) = 1:3;
sumLowSost(2:4, 2) = sum(statNumOfChangeLow(:, :, 1)');%98 ���
sumLowSost(2:4, 3) = sum(statNumOfChangeLow(:, :, 2)');%99 ���
sumLowSost(2:4, 4) = sum(statNumOfChangeLow(:, :, 3)');%00 ���
quantileHi_09 = sumHiSost;%������ - ������������, ������� - ����
quantileHi_09(2:4, 2:4) = ceil(sumHiSost(2:4, 2:4)*0.9);
quantileHi_095 = sumHiSost;%������ - ������������, ������� - ����
quantileHi_095(2:4, 2:4) = ceil(sumHiSost(2:4, 2:4)*0.95);
quantileLow_09 = sumLowSost;%������ - ������������, ������� - ����
quantileLow_09(2:4, 2:4) = ceil(sumLowSost(2:4, 2:4)*0.9);
quantileLow_095 = sumLowSost;%������ - ������������, ������� - ����
quantileLow_095(2:4, 2:4) = ceil(sumLowSost(2:4, 2:4)*0.95);
maxIntervalHi(1, :, 1) = [0 1998 1999 2000];%������ - ������������, ������� - ����, Z - ��������: 1 - 0,9, 2 - 0,95
maxIntervalHi(2:4, 1, 1) = 1:3;
maxIntervalHi(1, :, 2) = [0 1998 1999 2000];
maxIntervalHi(2:4, 1, 2) = 1:3;
maxIntervalLow(1, :, 1) = [0 1998 1999 2000];%������ - ������������, ������� - ����, Z - ��������: 1 - 0,9, 2 - 0,95
maxIntervalLow(2:4, 1, 1) = 1:3;
maxIntervalLow(1, :, 2) = [0 1998 1999 2000];
maxIntervalLow(2:4, 1, 2) = 1:3;
for i = 2:1:4%������������
    for j = 2:1:4%����
        sumHi09 = 0;
        sumHi095 = 0;
        indHi09 = 1;%���� 1 - ���� �����, 0 - ����� ��������
        indHi095 = 1;%0,95 - ������������ ��������
        sumLow09 = 0;
        sumLow095 = 0;
        indLow09 = 1;%���� 1 - ���� �����, 0 - ����� ��������
        indLow095 = 1;%0,95 - ������������ �������� 
        for k = 1:1:size(statNumOfChangeHi, 2)
            %������� �����
            if statNumOfChangeHi(i - 1, k, j - 1) && indHi095
                sumHi09 = sumHi09 + statNumOfChangeHi(i - 1, k, j - 1);
                sumHi095 = sumHi095 + statNumOfChangeHi(i - 1, k, j - 1);
            end
            if sumHi09 >= quantileHi_09(i, j) && indHi09
                maxIntervalHi(i, j, 1) = k;
                indHi09 = 0;
            end
            if sumHi095 >= quantileHi_095(i, j) && indHi095
                maxIntervalHi(i, j, 2) = k;
                indHi095 = 0;
            end
            %������� �����
            if statNumOfChangeLow(i - 1, k, j - 1) && indLow095
                sumLow09 = sumLow09 + statNumOfChangeLow(i - 1, k, j - 1);
                sumLow095 = sumLow095 + statNumOfChangeLow(i - 1, k, j - 1);
            end
            if sumLow09 >= quantileLow_09(i, j) && indLow09
                maxIntervalLow(i, j, 1) = k;
                indLow09 = 0;
            end
            if sumLow095 >= quantileLow_095(i, j) && indLow095
                maxIntervalLow(i, j, 2) = k;
                indLow095 = 0;
            end
        end
    end
end
clear sumHi09 sumHi095 indHi09 indHi095 sumLow09 sumLow095 indLow09 indLow095

%����� �������� 1-�� ������������� �������� �� ������ ���������� ���������
partOfFirstHi = sumHiSost;
partOfFirstLow = sumLowSost;
for i = 2:1:4%������������
    for j = 2:1:4
        partOfFirstHi(i, j) = 100*statNumOfChangeHi(i - 1, 1, j - 1)/sumHiSost(i, j);
        partOfFirstLow(i, j) = 100*statNumOfChangeLow(i - 1, 1, j - 1)/sumLowSost(i, j);
    end
end

%����� �������� 1-�� � ����- ������������� �������� �� ������ ���������� ���������
partOfFirstHi2 = sumHiSost;
partOfFirstLow2 = sumLowSost;
for i = 2:1:4%������������
    for j = 2:1:4
        partOfFirstHi2(i, j) = 100*(statNumOfChangeHi(i - 1, 1, j - 1) + statNumOfChangeHi(i - 1, 2, j - 1))/sumHiSost(i, j);
        partOfFirstLow2(i, j) = 100*(statNumOfChangeLow(i - 1, 1, j - 1) + statNumOfChangeLow(i - 1, 2, j - 1))/sumLowSost(i, j);
    end
end

save([PathFNameDataA0_1 '..\SearchNumOfChange.mat']);



%��� ������� ��� ���������
% axeTimeAcclrt = (0:stepTimeAcclrt:...
%     (size(DataAcclrt, 2)*stepTimeAcclrt)-stepTimeAcclrt)';
% clear stepTimeAcclrt

% figure(1);
% plot(axeTimeAcclrt, DataAcclrt(1, :), axeTimeAcclrt, hightDigit,...
%     axeTimeAcclrt, incor1, axeTimeAcclrt, incor2, 'LineWidth', 2);
% title('����������� ������������ ������� ���� ��������', 'FontName', 'Times New Roman',...
%     'FontSize', 14);
% xlabel('����� ������, �', 'FontName', 'Times New Roman', 'FontSize', 14);
% ylabel('��������', 'FontName', 'Times New Roman', 'FontSize', 14);
% set(gca, 'FontName', 'Times New Roman', 'FontSize', 14);
% hlegeng = legend('�������� ���������', '������� �����', '�������� ������� ����� 1', '�������� ������� ����� 2');
% set(hlegeng, 'FontName', 'Times New Roman', 'FontSize', 14);
