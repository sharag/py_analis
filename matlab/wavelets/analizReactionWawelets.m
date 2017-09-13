%% Анализ реакции вейвлетов на типовые скачки
clc
clear
%% Скачки
for k=1
sizeOfhop = 100;
% единичный скачок
hops = zeros(4,sizeOfhop);sizehops = zeros(1,4);
sizehops(1) = sizeOfhop; hops(1,floor(sizeOfhop/2):sizeOfhop) = 1;
sizehops(2) = sizeOfhop; hops(2,:) = (hops(1,:)-0.5)*2;
sizehops(3) = sizeOfhop; hops(3,:) = 1-hops(1,:);
sizehops(4) = sizeOfhop; hops(4,:) = (hops(1,:)-0.5)*2;
end
%% Параметры вейвлет-анализа
for k=1
LvlDec = 3;% Уровень разложения
NiterW = 10;% Количество итераций вычисления вейвлета
Fd = sizeOfhop;% Частота следования отсчетов в секунду
stepTimeData = 1/Fd;%Шаг временной сетки для последовательности
wavelet = 'db12';% Выбор вейвлета
EntType = 'shannon';% Тип энтропии
stepFreq = 1;% Шаг изменения частоты для CWT в Гц
timeHop = (0:(length(hops(1,:))-1))/Fd;% Ось времени
end
%% Определение центральной частоты выбранного вейвлета
for k=1
numFig = 1;headFig(numFig) = figure(numFig); %#ok<*SAGROW>
centrFreq = centfrq(wavelet,NiterW,'plot');
set(gcf,'name',['Определение центральной частоты вейвлета: ' wavelet],'Visible','on');
title(['Центральная частота вейвлета ' wavelet ': ' num2str(centrFreq)...
    'Гц, период: ' num2str(1/centrFreq) ' c'],'FontName','Times New Roman','FontSize',12);
xlabel('Промежуток носителя','FontName','Times New Roman','FontSize',12);
ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
% Вывод центральных частот для различных уровней разложения
FreqLvl = zeros(1,LvlDec);
for i = 1:LvlDec
    FreqLvl(i) = centrFreq*Fd/(2^(i - 1));
    display(['Центральная частота для ' num2str(i) '-го уровня разложения: ' num2str(FreqLvl(i)) ' Гц.']);
end
end
%% Многоуровневое разложение wavedec
for k=1
[CoefWD,LenCoefWD] = wavedec(hops(1,:),LvlDec,wavelet);
coefAppWD = appcoef(CoefWD,LenCoefWD,wavelet,LvlDec);
coefDetWD = zeros(LvlDec,max(LenCoefWD));
stepTimeDetCoefsWD = zeros(1,LvlDec);
for i = 1:LvlDec
    temp = detcoef(CoefWD,LenCoefWD,i);
    coefDetWD(i,1:length(temp)) = temp(:);
    stepTimeDetCoefsWD(i) = length(hops(1,:))/LenCoefWD(LvlDec+2-i)/Fd;% Время для разных уровней разложения
    clear temp
end
clear Coef
end
%% Прямое восстановление отдельно по каждому набору детализирующих коэффициентов
for i = LvlDec:-1:1
    temp = upcoef('d',coefDetWD(i,1:LenCoefWD(LvlDec+2-i)),wavelet,i);
    recnstrSig(i, 1:length(temp)) = temp(:);
    sizeRecnstrSig(i) = length(temp);
    stepTrecnstrSig(i) = length(hops(1,:))/sizeRecnstrSig(i)/Fd;% Время для разных уровней разложения
    clear temp
end
%% Пакетное разложение wpdec
%CoefWPD

%% Графики скачка и аппроксимирующих коэффициентов
for k=1
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','Графики скачка и аппроксимирующих коэффициентов','Visible','on');
subplot(2,1,1);plot(timeHop,hops(1,:),'LineWidth',2);
title('График скачка','FontName','Times New Roman','FontSize',12);
xlabel('\it t, с','FontName','Times New Roman','FontSize',12);
ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
subplot(2,1,2);plot((0:(LenCoefWD(1)-1))*sizehops(1)/Fd/LenCoefWD(1),coefAppWD,'LineWidth',2);
title('График аппроксимирующих коэффициентов','FontName','Times New Roman','FontSize',12);
xlabel('\it t, с','FontName','Times New Roman','FontSize',12);
ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
end
%% Графики скачка и детализирующих коэффициентов
for k=1
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','Графики скачка и детализирующих коэффициентов','Visible','on');
subplot(LvlDec+1,1,1);plot(timeHop,hops(1,:),'LineWidth',2);
title('График скачка','FontName','Times New Roman','FontSize',12);
xlabel('\it t, с','FontName','Times New Roman','FontSize',12);
ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
set(gca,'FontName','Times New Roman','FontSize',12);
for i = 1:LvlDec
    subplot(LvlDec+1,1,i+1);
    plot((0:(LenCoefWD(LvlDec+2-i)-1))*stepTimeDetCoefsWD(i),coefDetWD(i,1:LenCoefWD(LvlDec+2-i)),'LineWidth',2);
    title(['График детализирующих коэффициентов ' num2str(i) ' уровня'],'FontName',...
        'Times New Roman','FontSize',12);
    xlabel('\it t, с','FontName','Times New Roman','FontSize',12);
    ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
    set(gca,'FontName','Times New Roman','FontSize',12);
end
end
%% График восстановленных компонент сигнала для разных уровней
for k=1
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','Восстановленные компоненты','Visible','on');
for i = 1:LvlDec
    subplot(LvlDec,1,i);
    plot((0:(sizeRecnstrSig(i)-1))*stepTrecnstrSig(i),recnstrSig(i,1:sizeRecnstrSig(i)),'LineWidth',2);
    title(['Восстановленная компонента уровня ' num2str(i) ' (средняя частота: ' num2str(FreqLvl(i)) ' Гц.)'],...
        'FontName','Times New Roman','FontSize',12);
    xlabel('\it t, с','FontName','Times New Roman','FontSize',12);
    ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
    set(gca, 'FontName','Times New Roman','FontSize',12);
end
end
%% Статистические харатеристики восстановленных компонент
for k=1
meanValRS=zeros(1,LvlDec);dispersValRS=zeros(1,LvlDec);SKOvalRS=zeros(1,LvlDec);
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','АКФ восстановленных компонент','Visible','on');
for i = 1:LvlDec
    meanValRS(i) = mean(recnstrSig(i,1:sizeRecnstrSig(i)));
    dispersValRS(i) = var(recnstrSig(i,1:sizeRecnstrSig(i)));
    SKOvalRS(i) = std(recnstrSig(i,1:sizeRecnstrSig(i)));
    [tempAKFRS, tempLagsRS] = xcorr(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    AKFRS(i,1:length(tempAKFRS)) = tempAKFRS(:);
    AKFtimeRS(i,1:length(tempLagsRS)) = tempLagsRS;
    AKFlensRS(i)=length(tempAKFRS);
    disp(['М.О. детализирующих коэффициентов ' num2str(i) ...
        ' уровня разложения:' num2str(meanValRS(i)) '.']);
    disp(['Дисперсия детализирующих коэффициентов ' num2str(i) ...
        ' уровня разложения:' num2str(dispersValRS(i)) '.']);
    disp(['СКО детализирующих коэффициентов ' num2str(i) ...
        ' уровня разложения:' num2str(SKOvalRS(i)) '.']);
    subplot(LvlDec,1,i);
    plot(AKFtimeRS(i,1:AKFlensRS(i))*sizehops(1)*2/Fd/AKFlensRS(i),AKFRS(i,1:AKFlensRS(i)),...
        'LineWidth',2);
    title(['АКФ восстановленной компоненты уровня ' num2str(i)],...
        'FontName','Times New Roman','FontSize',12);
    xlabel('Смещение, с','FontName','Times New Roman','FontSize',12);
    ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
    set(gca, 'FontName','Times New Roman','FontSize',12);
    clear tempAKFRS tempLagsRS
end
end

%% Статистические характеристики детализирующих коэффициентов
for k=1
meanVal=zeros(1,LvlDec);dispersVal=zeros(1,LvlDec);SKOval=zeros(1,LvlDec);
numFig = numFig+1;headFig(numFig) = figure(numFig);
set(gcf,'Name','АКФ детализирующих коэффициентов','Visible','on');
for i = 1:LvlDec
    meanVal(i) = mean(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    dispersVal(i) = var(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    SKOval(i) = std(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    [tempAKF, tempLags] = xcorr(coefDetWD(i,1:LenCoefWD(LvlDec+2-i)));
    AKF(i,1:length(tempAKF)) = tempAKF(:);
    AKFtime(i,1:length(tempLags)) = tempLags;
    AKFlens(i)=length(tempAKF);
    disp(['М.О. детализирующих коэффициентов ' num2str(i) ...
        ' уровня разложения:' num2str(meanVal(i)) '.']);
    disp(['Дисперсия детализирующих коэффициентов ' num2str(i) ...
        ' уровня разложения:' num2str(dispersVal(i)) '.']);
    disp(['СКО детализирующих коэффициентов ' num2str(i) ...
        ' уровня разложения:' num2str(SKOval(i)) '.']);
    subplot(LvlDec,1,i);
    plot(AKFtime(i,1:AKFlens(i))*sizehops(1)*2/Fd/AKFlens(i),AKF(i,1:AKFlens(i)),'LineWidth',2);
    title(['АКФ детализирующих коэффициентов уровня ' num2str(i)],...
        'FontName','Times New Roman','FontSize',12);
    xlabel('Смещение, с','FontName','Times New Roman','FontSize',12);
    ylabel('Амплитуда','FontName','Times New Roman','FontSize',12);
    set(gca, 'FontName','Times New Roman','FontSize',12);
    clear tempAKF tempLags
end
end
%% CWT
% Расчет шкалы масштабного параметра
% stepScale = FreqLvl(1)/(FreqLvl(1) - stepFreq);
% i = 1;
% scale(1) = 1;
% while (FreqLvl(1)/scale(i)) > 1
%     i = i + 1;
%     scale(i) = stepScale^(i - 1);
% end
% 







%fprintf(infofileID, ['Центральная частота для ' num2str(i) '-го уровня разложения: ' num2str(FreqLvl(i)) ' Гц.\n\r']);
%saveas(headFig(numFig),['e:\MATscripts\wavelets\rezults\CentrFreqWawelet_' wavelet],'jpg');
%xlswrite([pathREZ 'Freq_lvl.xls'], FreqLvl);