%% ������ ������� ��������� �� ������� ������
clc
clear
%% ������
for k=1
sizeOfhop = 100;
% ��������� ������
hops = zeros(4,sizeOfhop);sizehops = zeros(1,4);
sizehops(1) = sizeOfhop; hops(1,floor(sizeOfhop/2):sizeOfhop) = 1;
sizehops(2) = sizeOfhop; hops(2,:) = (hops(1,:)-0.5)*2;
sizehops(3) = sizeOfhop; hops(3,:) = 1-hops(1,:);
sizehops(4) = sizeOfhop; hops(4,:) = (hops(1,:)-0.5)*2;
end
%% ��������� �������-�������
for k=1
LvlDec = 3;% ������� ����������
NiterW = 10;% ���������� �������� ���������� ��������
Fd = sizeOfhop;% ������� ���������� �������� � �������
stepTimeData = 1/Fd;%��� ��������� ����� ��� ������������������
wavelet = 'db12';% ����� ��������
EntType = 'shannon';% ��� ��������
stepFreq = 1;% ��� ��������� ������� ��� CWT � ��
timeHop = (0:(length(hops(1,:))-1))/Fd;% ��� �������
end
%% ����������� ����������� ������� ���������� ��������
for k=1
numFig = 1;headFig(numFig) = figure(numFig); %#ok<*SAGROW>
centrFreq = centfrq(wavelet,NiterW,'plot');
set(gcf,'name',['����������� ����������� ������� ��������: ' wavelet],'Visible','on');
title(['����������� ������� �������� ' wavelet ': ' num2str(centrFreq)...
    '��, ������: ' num2str(1/centrFreq) ' c'],'FontName','Times New Roman','FontSize',12);
xlabel('���������� ��������','FontName','Times New Roman','FontSize',12);
ylabel('���������','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
% ����� ����������� ������ ��� ��������� ������� ����������
FreqLvl = zeros(1,LvlDec);
for i = 1:LvlDec
    FreqLvl(i) = centrFreq*Fd/(2^(i - 1));
    display(['����������� ������� ��� ' num2str(i) '-�� ������ ����������: ' num2str(FreqLvl(i)) ' ��.']);
end
end
%% �������������� ���������� wavedec
for k=1
[CoefWD,LenCoefWD] = wavedec(hops(1,:),LvlDec,wavelet);
coefAppWD = appcoef(CoefWD,LenCoefWD,wavelet,LvlDec);
coefDetWD = zeros(LvlDec,max(LenCoefWD));
stepTimeDetCoefsWD = zeros(1,LvlDec);
for i = 1:LvlDec
    temp = detcoef(CoefWD,LenCoefWD,i);
    coefDetWD(i,1:length(temp)) = temp(:);
    stepTimeDetCoefsWD(i) = length(hops(1,:))/LenCoefWD(LvlDec+2-i)/Fd;% ����� ��� ������ ������� ����������
    clear temp
end
clear Coef
end
%% ������ �������������� �������� �� ������� ������ �������������� �������������
for i = LvlDec:-1:1
    temp = upcoef('d',coefDetWD(i,1:LenCoefWD(LvlDec+2-i)),wavelet,i);
    recnstrSig(i, 1:length(temp)) = temp(:);
    sizeRecnstrSig(i) = length(temp);
    stepTrecnstrSig(i) = length(hops(1,:))/sizeRecnstrSig(i)/Fd;% ����� ��� ������ ������� ����������
    clear temp
end
%% �������� ���������� wpdec
%CoefWPD

%% ������� ������ � ���������������� �������������
for k=1
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','������� ������ � ���������������� �������������','Visible','on');
subplot(2,1,1);plot(timeHop,hops(1,:),'LineWidth',2);
title('������ ������','FontName','Times New Roman','FontSize',12);
xlabel('\it t, �','FontName','Times New Roman','FontSize',12);
ylabel('���������','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
subplot(2,1,2);plot((0:(LenCoefWD(1)-1))*sizehops(1)/Fd/LenCoefWD(1),coefAppWD,'LineWidth',2);
title('������ ���������������� �������������','FontName','Times New Roman','FontSize',12);
xlabel('\it t, �','FontName','Times New Roman','FontSize',12);
ylabel('���������','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
end
%% ������� ������ � �������������� �������������
for k=1
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','������� ������ � �������������� �������������','Visible','on');
subplot(LvlDec+1,1,1);plot(timeHop,hops(1,:),'LineWidth',2);
title('������ ������','FontName','Times New Roman','FontSize',12);
xlabel('\it t, �','FontName','Times New Roman','FontSize',12);
ylabel('���������','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
for i = 1:LvlDec
    subplot(LvlDec+1,1,i+1);
    plot((0:(LenCoefWD(LvlDec+2-i)-1))*stepTimeDetCoefsWD(i),coefDetWD(i,1:LenCoefWD(LvlDec+2-i)),'LineWidth',2);
    title(['������ �������������� ������������� ' num2str(i) ' ������'],'FontName',...
        'Times New Roman','FontSize',12);
    xlabel('\it t, �','FontName','Times New Roman','FontSize',12);
    ylabel('���������','FontName','Times New Roman','FontSize',12);
    set(gca,'FontName','Times New Roman','FontSize',12);
end
end
%% ������ ��������������� ��������� ������� ��� ������ �������
for k=1
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','��������������� ����������','Visible','on');
for i = 1:LvlDec
    subplot(LvlDec,1,i);
    plot((0:(sizeRecnstrSig(i)-1))*stepTrecnstrSig(i),recnstrSig(i,1:sizeRecnstrSig(i)),'LineWidth',2);
    title(['��������������� ���������� ������ ' num2str(i) ' (������� �������: ' num2str(FreqLvl(i)) ' ��.)'],...
        'FontName','Times New Roman','FontSize',12);
    xlabel('\it t, �','FontName','Times New Roman','FontSize',12);
    ylabel('���������','FontName','Times New Roman','FontSize',12);
    set(gca, 'FontName','Times New Roman','FontSize',12);
end
end
%% �������������� ������������� ��������������� ���������
for k=1
meanValRS=zeros(1,LvlDec);dispersValRS=zeros(1,LvlDec);SKOvalRS=zeros(1,LvlDec);
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','��� ��������������� ���������','Visible','on');
for i = 1:LvlDec
    meanValRS(i) = mean(recnstrSig(i,1:sizeRecnstrSig(i)));
    dispersValRS(i) = var(recnstrSig(i,1:sizeRecnstrSig(i)));
    SKOvalRS(i) = std(recnstrSig(i,1:sizeRecnstrSig(i)));
    [tempAKFRS, tempLagsRS] = xcorr(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    AKFRS(i,1:length(tempAKFRS)) = tempAKFRS(:);
    AKFtimeRS(i,1:length(tempLagsRS)) = tempLagsRS;
    AKFlensRS(i)=length(tempAKFRS);
    disp(['�.�. �������������� ������������� ' num2str(i) ...
        ' ������ ����������:' num2str(meanValRS(i)) '.']);
    disp(['��������� �������������� ������������� ' num2str(i) ...
        ' ������ ����������:' num2str(dispersValRS(i)) '.']);
    disp(['��� �������������� ������������� ' num2str(i) ...
        ' ������ ����������:' num2str(SKOvalRS(i)) '.']);
    subplot(LvlDec,1,i);
    plot(AKFtimeRS(i,1:AKFlensRS(i))*sizehops(1)*2/Fd/AKFlensRS(i),AKFRS(i,1:AKFlensRS(i)),...
        'LineWidth',2);
    title(['��� ��������������� ���������� ������ ' num2str(i)],...
        'FontName','Times New Roman','FontSize',12);
    xlabel('��������, �','FontName','Times New Roman','FontSize',12);
    ylabel('���������','FontName','Times New Roman','FontSize',12);
    set(gca, 'FontName','Times New Roman','FontSize',12);
    clear tempAKFRS tempLagsRS
end
end

%% �������������� �������������� �������������� �������������
for k=1
meanVal=zeros(1,LvlDec);dispersVal=zeros(1,LvlDec);SKOval=zeros(1,LvlDec);
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','��� �������������� �������������','Visible','on');
for i = 1:LvlDec
    meanVal(i) = mean(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    dispersVal(i) = var(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    SKOval(i) = std(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    [tempAKF, tempLags] = xcorr(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    AKF(i,1:length(tempAKF)) = tempAKF(:);
    AKFtime(i,1:length(tempLags)) = tempLags;
    AKFlens(i)=length(tempAKF);
    disp(['�.�. �������������� ������������� ' num2str(i) ...
        ' ������ ����������:' num2str(meanVal(i)) '.']);
    disp(['��������� �������������� ������������� ' num2str(i) ...
        ' ������ ����������:' num2str(dispersVal(i)) '.']);
    disp(['��� �������������� ������������� ' num2str(i) ...
        ' ������ ����������:' num2str(SKOval(i)) '.']);
    subplot(LvlDec,1,i);
    plot(AKFtime(i,1:AKFlens(i))*sizehops(1)*2/Fd/AKFlens(i),AKF(i,1:AKFlens(i)),'LineWidth',2);
    title(['��� �������������� ������������� ������ ' num2str(i)],...
        'FontName','Times New Roman','FontSize',12);
    xlabel('��������, �','FontName','Times New Roman','FontSize',12);
    ylabel('���������','FontName','Times New Roman','FontSize',12);
    set(gca, 'FontName','Times New Roman','FontSize',12);
    clear tempAKF tempLags
end
end
%% CWT
% ������ ����� ����������� ���������
% stepScale = FreqLvl(1)/(FreqLvl(1) - stepFreq);
% i = 1;
% scale(1) = 1;
% while (FreqLvl(1)/scale(i)) > 1
%     i = i + 1;
%     scale(i) = stepScale^(i - 1);
% end
% 







%fprintf(infofileID, ['����������� ������� ��� ' num2str(i) '-�� ������ ����������: ' num2str(FreqLvl(i)) ' ��.\n\r']);
%saveas(headFig(numFig),['e:\MATscripts\wavelets\rezults\CentrFreqWawelet_' wavelet],'jpg');
%xlswrite([pathREZ 'Freq_lvl.xls'], FreqLvl);