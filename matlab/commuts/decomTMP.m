xlsFname = [fpath '98.xlsx'];
%% ������ � ������� ����� ������
B98 = 28.900777;
L98 = -76.104993;
B99 = 28.88868;
L99 = -76.111116;
B00 = 28.906731;
L00 = -76.109304;
Bstart = B98;
Lstart = L98;

%% ������� �������� �� ������������� � ��������� ����������� ��
Mngr_nav98 = [0.01499694,-0.00344509,-0.00271363;...
    0.00034282,-0.00871783,0.01296235;...
    -0.00437206,-0.01250086,-0.00829183];
Mngr_nav99 = [0.01523885,-0.00339881,0.00060525;...
    -0.00250942,-0.00902408,0.01250638;...
    -0.00237087,-0.0122945,-0.00934692];
Mngr_nav00 = [0.01509545,-0.00381095,0.00132082;...
    -0.00327806,-0.00861095,0.01261929;...
    0.00234995,-0.01246871,-0.00911864];
Mngr_nav=Mngr_nav98;

%% ������
mode_D = zeros(1,length(comm_d1(:,12)));
for i=1:length(comm_d1(:,12))
    mode_D(i) = formValue(comm_d1(i,12),12,5);
end
mode_D = medfilt1(getN2C(mode_D,5),3);
axeX100_D=0.01:0.01:(length(mode_D)*0.01);
figure('Name', '����� ������� D-�����');
plot(axeX100_D,mode_D,'LineWidth',2);title('����� ������� D-�����');xlabel('�����,�');ylabel('MODE_D');
writetable(table(mode_D',axeX100_D','VariableNames',{'mode' 'time'}),xlsFname,'Sheet','Mode_D');

%% �������� �10, �11 D-�����
indC10 = zeros(1,length(comm_d1(:,56)));
indC11 = zeros(1,length(comm_d1(:,57)));
for i=1:length(comm_d1(:,56))
    indC10(i) = formValue(comm_d1(i,56),1,4);
    indC11(i) = formValue(comm_d1(i,57),1,6);
end

%% ������ ����� A-�����
mode_A=zeros(1,length(GTS_Aline(:,1)));
for i=1:length(GTS_Aline(:,1))
    mode_A(i) = formValue(GTS_Aline(i,181),6,3);
end
mode_A = medfilt1(mode_A,5);
axeX400_A = (1/400):(1/400):(length(mode_A)*(1/400));
figure('Name', '����� ������� A-�����');
plot(axeX400_A,mode_A','LineWidth',2);title('����� ������� A-�����');xlabel('�����,�');ylabel('MODE_A');

%% ������� �������� �� ������������� � ��������� ������� ���������
Mnav_svSK = zeros(3,3,length(comm_d1(:,24))); 
Mnav_svSK(1,1,:) = medfilt1(getN2C(comm_d1(:,24),16),3); 
Mnav_svSK(1,2,:) = medfilt1(getN2C(comm_d1(:,25),16),3);
Mnav_svSK(1,3,:) = medfilt1(getN2C(comm_d1(:,26),16),3);
Mnav_svSK(2,1,:) = medfilt1(getN2C(comm_d1(:,27),16),3);
Mnav_svSK(2,2,:) = medfilt1(getN2C(comm_d1(:,28),16),3);
Mnav_svSK(2,3,:) = medfilt1(getN2C(comm_d1(:,29),16),3);
Mnav_svSK(3,1,:) = medfilt1(getN2C(comm_d1(:,30),16),3);
Mnav_svSK(3,2,:) = medfilt1(getN2C(comm_d1(:,31),16),3);
Mnav_svSK(3,3,:) = medfilt1(getN2C(comm_d1(:,32),16),3);
Mnav_svSK_plot = zeros(9,length(comm_d1(:,24)));
Mnav_svSK_plot(1,:) = medfilt1(getN2C(comm_d1(:,24),16),3); 
Mnav_svSK_plot(2,:) = medfilt1(getN2C(comm_d1(:,25),16),3);
Mnav_svSK_plot(3,:) = medfilt1(getN2C(comm_d1(:,26),16),3);
Mnav_svSK_plot(4,:) = medfilt1(getN2C(comm_d1(:,27),16),3);
Mnav_svSK_plot(5,:) = medfilt1(getN2C(comm_d1(:,28),16),3);
Mnav_svSK_plot(6,:) = medfilt1(getN2C(comm_d1(:,29),16),3);
Mnav_svSK_plot(7,:) = medfilt1(getN2C(comm_d1(:,30),16),3);
Mnav_svSK_plot(8,:) = medfilt1(getN2C(comm_d1(:,31),16),3);
Mnav_svSK_plot(9,:) = medfilt1(getN2C(comm_d1(:,32),16),3);
figure('Name', '������� �������� �� ������������� � ��������� ������� ���������');
plot(axeX100_D,Mnav_svSK_plot(1,:),axeX100_D,Mnav_svSK_plot(2,:),axeX100_D,Mnav_svSK_plot(3,:),...
    axeX100_D,Mnav_svSK_plot(4,:),axeX100_D,Mnav_svSK_plot(5,:),axeX100_D,Mnav_svSK_plot(6,:),...
    axeX100_D,Mnav_svSK_plot(7,:),axeX100_D,Mnav_svSK_plot(8,:),axeX100_D,Mnav_svSK_plot(8,:),'LineWidth',2);
title('������� �������� �� ������������� � ��������� ������� ���������');xlabel('�����,�');ylabel('M');
clear Mnav_svSK_plot 

%% ������������ ���������� ��������� � ������������� �� �� D-�����
accelNavSK_D = zeros(3,length(comm_d1(:,58)));
for i=1:length(comm_d1(:,58))
    accelNavSK_D(1,i) = formValue([comm_d1(i,59), comm_d1(i,58)],[1, 1],[16,16]);
    accelNavSK_D(2,i) = formValue([comm_d1(i,61), comm_d1(i,60)],[1, 1],[16,16]);
    accelNavSK_D(3,i) = formValue([comm_d1(i,63), comm_d1(i,62)],[1, 1],[16,16]);
end
accelNavSK_D(1,:) = medfilt1(getN2C(accelNavSK_D(1,:),32),3);
accelNavSK_D(2,:) = medfilt1(getN2C(accelNavSK_D(2,:),32),3);
accelNavSK_D(3,:) = medfilt1(medfilt1(getN2C(accelNavSK_D(3,:),32),3),3);
figure('Name', '������������ ���������� ��������� � ������������� �� �� D-�����');
plot(axeX100_D,accelNavSK_D(1,:),axeX100_D,accelNavSK_D(2,:),axeX100_D,accelNavSK_D(3,:),'LineWidth',2);
title('������������ ���������� ��������� � ������������� �� �� D-�����');xlabel('�����,�');ylabel('accelNavSK_D');
T = table(accelNavSK_D(1,:)',accelNavSK_D(2,:)',accelNavSK_D(3,:)',...
    axeX100_D','VariableNames',{'UskorA0navSK' 'UskorA1navSK' 'UskorA2navSK' 'time'});
writetable(T,xlsFname,'Sheet','UskorNavSK_D');
clear T

%% ������������ ���������� ��������� � ������������� �� �� D-����� #2
findInd_3_5_7 = find(indC11==9);
numfr_3_5_7 = zeros(size(findInd_3_5_7));
for i=1:length(findInd_3_5_7)
    [val, ind] = min(findInd_3_5_7);
    findInd_3_5_7(ind) = [];
    numfr_3_5_7(i) = val;
end
findInd_72_74_76 = find(indC11==35);
numfr_72_74_76 = zeros(size(findInd_72_74_76));
for i=1:length(findInd_72_74_76)
    [val, ind] = min(findInd_72_74_76);
    findInd_72_74_76(ind) = [];
    numfr_72_74_76(i) = val;
end
clear findInd_72_74_76 findInd_3_5_7
% ������������ � ������ ���������, ������������ ��� X
accelNavSK_D_AxeX = zeros(1,(length(numfr_3_5_7)+length(numfr_72_74_76)));
accelNavSK_D_ = zeros(3,(length(numfr_3_5_7)+length(numfr_72_74_76)));
for i=1:(length(numfr_3_5_7)+length(numfr_72_74_76))
    if isempty(numfr_72_74_76)
        [val, ind] = min(numfr_3_5_7);
        accelNavSK_D_(1,i)=formValue([comm_d1(val,4), comm_d1(val,3)],[1, 1],[16,16]);
        accelNavSK_D_(2,i)=formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]);
        accelNavSK_D_(3,i)=formValue([comm_d1(val,8), comm_d1(val,7)],[1, 1],[16,16]);
        accelNavSK_D_AxeX(i)=min(numfr_3_5_7)*0.01;
        numfr_3_5_7(ind)=[];
        continue
    end
    if isempty(numfr_3_5_7)
        [val, ind] = min(numfr_72_74_76);
        accelNavSK_D_(1,i)=formValue([comm_d1(val,73), comm_d1(val,72)],[1, 1],[16,16]);
        accelNavSK_D_(2,i)=formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]);
        accelNavSK_D_(3,i)=formValue([comm_d1(val,77), comm_d1(val,76)],[1, 1],[16,16]);
        accelNavSK_D_AxeX(i)=min(numfr_72_74_76)*0.01;
        numfr_72_74_76(ind)=[];
        continue
    end
    if min(numfr_3_5_7)<min(numfr_72_74_76)
        [val, ind] = min(numfr_3_5_7);
        accelNavSK_D_(1,i)=formValue([comm_d1(val,4), comm_d1(val,3)],[1, 1],[16,16]);
        accelNavSK_D_(2,i)=formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]);
        accelNavSK_D_(3,i)=formValue([comm_d1(val,8), comm_d1(val,7)],[1, 1],[16,16]);
        accelNavSK_D_AxeX(i)=min(numfr_3_5_7)*0.01;
        numfr_3_5_7(ind)=[];
    else
        [val, ind] = min(numfr_72_74_76);
        accelNavSK_D_(1,i)=formValue([comm_d1(val,73), comm_d1(val,72)],[1, 1],[16,16]);
        accelNavSK_D_(2,i)=formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]);
        accelNavSK_D_(3,i)=formValue([comm_d1(val,77), comm_d1(val,76)],[1, 1],[16,16]);
        accelNavSK_D_AxeX(i)=min(numfr_72_74_76)*0.01;
        numfr_72_74_76(ind)=[];
    end
end
clear ind val numfr_3_5_7 numfr_72_74_76
accelNavSK_D_(1,:)=medfilt1(getN2C(accelNavSK_D_(1,:),32),3);
accelNavSK_D_(2,:)=medfilt1(getN2C(accelNavSK_D_(2,:),32),3);
accelNavSK_D_(3,:)=medfilt1(getN2C(accelNavSK_D_(3,:),32),3);
figure('Name', '������������ ���������� ��������� � ������������� �� �� D-����� #2');
plot(accelNavSK_D_AxeX,accelNavSK_D_(1,:),accelNavSK_D_AxeX,accelNavSK_D_(2,:),accelNavSK_D_AxeX,accelNavSK_D_(3,:),'LineWidth',2);
title('������������ ���������� ��������� � ������������� �� �� D-����� #2');xlabel('�����,�');ylabel('accelNavSK_D_');

%% ������������ ���������� ��������� � ��������� ��
accelSvSK = zeros(3,length(comm_d1(:,58)));
for i=1:length(comm_d1(:,58))
    accelSvSK(:,i) = Mnav_svSK(:,:,i)*accelNavSK_D(:,i);
end
figure('Name', '������������ ���������� ��������� � ��������� ��');
plot(axeX100_D,accelSvSK(1,:),axeX100_D,accelSvSK(2,:),axeX100_D,accelSvSK(3,:),'LineWidth',2);
title('������������ ���������� ��������� � ��������� ��');xlabel('�����,�');ylabel('accelSvSK');
T = table(accelSvSK(1,:)',accelSvSK(2,:)',accelSvSK(3,:)',...
    axeX100_D','VariableNames',{'UskorA0svSK' 'UskorA1svSK' 'UskorA2svSK' 'time'});
writetable(T,xlsFname,'Sheet','UskorSvSK');
clear T

%% ������������ ���������� ��������� � ������������� �� �� �-�����
accelNavSK_A = zeros(3,length(GTS_Aline(:,1)));
for i=1:length(GTS_Aline(:,1))
    if mode_A(i)==0
        accelNavSK_A(1,i) = formValue([GTS_Aline(i,173), GTS_Aline(i,137)],[1, 1],[8,8]);
        accelNavSK_A(2,i) = formValue([GTS_Aline(i,237), GTS_Aline(i,217)],[1, 1],[8,8]);
        accelNavSK_A(3,i) = formValue([GTS_Aline(i,307), GTS_Aline(i,302)],[1, 1],[8,8]);
    end
    if mode_A(i)==1
        accelNavSK_A(1,i) = formValue([GTS_Aline(i,231), GTS_Aline(i,217)],[1, 1],[8,8]);
        accelNavSK_A(2,i) = formValue([GTS_Aline(i,273), GTS_Aline(i,237)],[1, 1],[8,8]);
        accelNavSK_A(3,i) = formValue([GTS_Aline(i,342), GTS_Aline(i,288)],[1, 1],[8,8]);
    end
    if mode_A(i)==3
        accelNavSK_A(1,i) = formValue([GTS_Aline(i,217), GTS_Aline(i,143)],[1, 1],[8,8]);
        accelNavSK_A(2,i) = formValue([GTS_Aline(i,237), GTS_Aline(i,231)],[1, 1],[8,8]);
        accelNavSK_A(3,i) = formValue([GTS_Aline(i,267), GTS_Aline(i,255)],[1, 1],[8,8]);
    end
    if mode_A(i)==7
        accelNavSK_A(1,i) = formValue([GTS_Aline(i,72), GTS_Aline(i,66)],[1, 1],[8,8]);
        accelNavSK_A(2,i) = formValue([GTS_Aline(i,217), GTS_Aline(i,143)],[1, 1],[8,8]);
        accelNavSK_A(3,i) = formValue([GTS_Aline(i,237), GTS_Aline(i,231)],[1, 1],[8,8]);
    end
end
accelNavSK_A(1,:)=medfilt1(getN2C(accelNavSK_A(1,:),16),3);
accelNavSK_A(2,:)=medfilt1(getN2C(accelNavSK_A(2,:),16),3);
accelNavSK_A(3,:)=medfilt1(getN2C(accelNavSK_A(3,:),16),3);
figure('Name', '������������ ���������� ��������� � ������������� �� �� �-�����');
plot(axeX400_A,accelNavSK_A(1,:),axeX400_A,accelNavSK_A(2,:),axeX400_A,accelNavSK_A(3,:),'LineWidth',2);
title('������������ ���������� ��������� � ������������� �� �� �-�����');xlabel('�����,�');ylabel('accelNavSK_A');

%% ������������  ��������� � ��������� ����������� �� �� �-�����
accelNGrSK_A = zeros(3,length(accelNavSK_A(1,:)));
for i=1:length(accelNGrSK_A(1,:))
    accelNGrSK_A(:,i) = Mngr_nav*accelNavSK_A(:,i);
end
figure('Name', '������������  ��������� � ��������� ����������� �� �� �-�����');
plot(axeX400_A,accelNGrSK_A(1,:),axeX400_A,accelNGrSK_A(2,:),...
    axeX400_A,accelNGrSK_A(3,:),'LineWidth',2);
title('������������  ��������� � ��������� ����������� �� �� �-�����');xlabel('�����,�');ylabel('accelNGrSK_A');
T = table(accelNGrSK_A(1,:)',accelNGrSK_A(2,:)',accelNGrSK_A(3,:)',...
    axeX400_A','VariableNames',{'UskorA0NGrSK' 'UskorA1NGrSK' 'UskorA2NGrSK' 'time'});
writetable(T,xlsFname,'Sheet','UskorNGrSK_A');
clear T

%% ������ ���������� ��������� 1, 2, 3 ������� ��� ���������� ����������
accelMod_D = medfilt1(getSign(comm_d1(:,21),16),3);
accelMod_navD = sqrt(accelNavSK_D(1,:).^2+accelNavSK_D(2,:).^2+accelNavSK_D(3,:).^2);
accelMod_SvSK = sqrt(accelSvSK(1,:).^2+accelSvSK(2,:).^2+accelSvSK(3,:).^2); 
accelMod_navA = sqrt(accelNavSK_A(1,:).^2+accelNavSK_A(2,:).^2+accelNavSK_A(3,:).^2);
accelMod_NGrA = sqrt(accelNGrSK_A(1,:).^2+accelNGrSK_A(2,:).^2+accelNGrSK_A(3,:).^2);
figure('Name', '������ ���������, ������������ � D-�����');
plot(axeX100_D,accelMod_D,'LineWidth',2);
title('������ ���������, ������������ � D-�����');xlabel('�����,�');ylabel('accelMod_D');
figure('Name', '������ ��������� �� ����������� ����� D-�����');
plot(axeX100_D,accelMod_navD,'LineWidth',2);
title('������ ��������� �� ����������� ����� D-�����');xlabel('�����,�');ylabel('accelMod_navD');
figure('Name', '������ ��������� �� ����������� ����');
plot(axeX100_D,accelMod_SvSK,'LineWidth',2);
title('������ ��������� �� ����������� ����');xlabel('�����,�');ylabel('accelMod_SvSK');
figure('Name', '������ ��������� �� ����������� ����� �-�����');
plot(axeX400_A,accelMod_navA,'LineWidth',2);
title('������ ��������� �� ����������� ����� �-�����');xlabel('�����,�');ylabel('accelMod_navA');
figure('Name', '������ ��������� �� ����������� �����');
plot(axeX400_A,accelMod_NGrA,'LineWidth',2);
title('������ ��������� �� ����������� �����');xlabel('�����,�');ylabel('accelMod_NGrA');

%% ������� ���������
% alfa = 1/298.25784; % ����������� ������ ��� (1/298.25784)
% as = 6378136; % ������� ������� ��� (6378136 �)
% extr = 2*alfa-alfa^2; % ������ �������������� ��������������� ������� ���;
% Nn = as/sqrt(1-(extr*(sin(Bstart)^2)));
% X = Nn*cos(Bstart*pi/180)*cos(Lstart*pi/180);
% Y = Nn*cos(Bstart*pi/180)*sin(Lstart*pi/180);
% Z = (Nn-extr*Nn)*sin(Bstart);
% MasshKoord = sqrt(X^2+Y^2+Z^2)/sqrt(koordNGrSK(1,1)^2+koordNGrSK(2,1)^2+koordNGrSK(3,1)^2);
% clear alfa as Nn X Y Z

%% ������������ ��������� � ������������� ��
% ����� ������� ������ � ������� ���������� �������� �11
findInd_3_5_7 = find(indC11==4);
findInd_3_5_7 = [findInd_3_5_7 find(indC11==22)];
findInd_3_5_7 = [findInd_3_5_7 find(indC11==37)];
numfr_3_5_7 = zeros(size(findInd_3_5_7));
for i=1:length(findInd_3_5_7)
    [val, ind] = min(findInd_3_5_7);
    findInd_3_5_7(ind) = [];
    numfr_3_5_7(i) = val;
end
findInd_72_74_76 = find(indC11==13);
findInd_72_74_76 = [findInd_72_74_76 find(indC11==30)];
findInd_72_74_76 = [findInd_72_74_76 find(indC11==48)];
numfr_72_74_76 = zeros(size(findInd_72_74_76));
for i=1:length(findInd_72_74_76)
    [val, ind] = min(findInd_72_74_76);
    findInd_72_74_76(ind) = [];
    numfr_72_74_76(i) = val;
end
clear findInd_72_74_76 findInd_3_5_7
% ������������ � ������ ���������, ������������ ��� X
koordNavSKAxeX = zeros(1,(length(numfr_3_5_7)+length(numfr_72_74_76)));
koordNavSK = zeros(3,(length(numfr_3_5_7)+length(numfr_72_74_76)));
for i=1:(length(numfr_3_5_7)+length(numfr_72_74_76))
    if isempty(numfr_72_74_76)
        [val, ind] = min(numfr_3_5_7);
        koordNavSK(1,i)=formValue([comm_d1(val,4), comm_d1(val,3)],[1, 1],[16,16]);
        koordNavSK(2,i)=formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]);
        koordNavSK(3,i)=formValue([comm_d1(val,8), comm_d1(val,7)],[1, 1],[16,16]);
        koordNavSKAxeX(i)=min(numfr_3_5_7)*0.01;
        numfr_3_5_7(ind)=[];
        continue
    end
    if isempty(numfr_3_5_7)
        [val, ind] = min(numfr_72_74_76);
        koordNavSK(1,i)=formValue([comm_d1(val,73), comm_d1(val,72)],[1, 1],[16,16]);
        koordNavSK(2,i)=formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]);
        koordNavSK(3,i)=formValue([comm_d1(val,77), comm_d1(val,76)],[1, 1],[16,16]);
        koordNavSKAxeX(i)=min(numfr_72_74_76)*0.01;
        numfr_72_74_76(ind)=[];
        continue
    end
    if min(numfr_3_5_7)<min(numfr_72_74_76)
        [val, ind] = min(numfr_3_5_7);
        koordNavSK(1,i)=formValue([comm_d1(val,4), comm_d1(val,3)],[1, 1],[16,16]);
        koordNavSK(2,i)=formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]);
        koordNavSK(3,i)=formValue([comm_d1(val,8), comm_d1(val,7)],[1, 1],[16,16]);
        koordNavSKAxeX(i)=min(numfr_3_5_7)*0.01;
        numfr_3_5_7(ind)=[];
    else
        [val, ind] = min(numfr_72_74_76);
        koordNavSK(1,i)=formValue([comm_d1(val,73), comm_d1(val,72)],[1, 1],[16,16]);
        koordNavSK(2,i)=formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]);
        koordNavSK(3,i)=formValue([comm_d1(val,77), comm_d1(val,76)],[1, 1],[16,16]);
        koordNavSKAxeX(i)=min(numfr_72_74_76)*0.01;
        numfr_72_74_76(ind)=[];
    end
end
clear ind val numfr_3_5_7 numfr_72_74_76
koordNavSK(1,:)=medfilt1(getN2C(koordNavSK(1,:),32),3);
koordNavSK(2,:)=medfilt1(getN2C(koordNavSK(2,:),32),3);
koordNavSK(3,:)=medfilt1(getN2C(koordNavSK(3,:),32),3);
figure('Name', '������������ ��������� � �����');
plot(koordNavSKAxeX,koordNavSK(1,:),koordNavSKAxeX,koordNavSK(2,:),...
    koordNavSKAxeX,koordNavSK(3,:),'LineWidth',2);
title('������������ ��������� � �����');xlabel('�����,�');ylabel('koordNavSK');
T = table(koordNavSK(1,:)',koordNavSK(2,:)',koordNavSK(3,:)',...
    koordNavSKAxeX','VariableNames',{'koordXnavSK' 'koordYnavSK' 'koordZnavSK' 'time'});
writetable(T,xlsFname,'Sheet','koordNavSK');
clear T

%% ������������ ��������� � ��������� ����������� ��
koordNGrSK = zeros(3,(length(koordNavSK(1,:))));
for i=1:length(koordNGrSK(1,:))
    % koordNGrSK(:,i) = Mngr_nav*(koordNavSK(:,i).*MasshKoord);
    koordNGrSK(:,i) = Mngr_nav*koordNavSK(:,i);
end
figure('Name', '������������ ��������� � �����');
plot(koordNavSKAxeX,koordNGrSK(1,:),koordNavSKAxeX,koordNGrSK(2,:),...
    koordNavSKAxeX,koordNGrSK(3,:),'LineWidth',2);
title('������������ ��������� � �����');xlabel('�����,�');ylabel('koordNGrSK');
T = table(koordNGrSK(1,:)',koordNGrSK(2,:)',koordNGrSK(3,:)',...
    koordNavSKAxeX','VariableNames',{'koordXNGrSK' 'koordYNGrSK' 'koordZNGrSK' 'time'});
writetable(T,xlsFname,'Sheet','koordNGrSK');
clear T

%% ������������ �������� �������� � ������������� ��
% ����� ������� ������ � ������� ���������� �������� �11
findInd_3_5_7 = find(indC11==5);
findInd_3_5_7 = [findInd_3_5_7 find(indC11==23)];
findInd_3_5_7 = [findInd_3_5_7 find(indC11==38)];
numfr_3_5_7 = zeros(size(findInd_3_5_7));
for i=1:length(findInd_3_5_7)
    [val, ind] = min(findInd_3_5_7);
    findInd_3_5_7(ind) = [];
    numfr_3_5_7(i) = val;
end
findInd_72_74_76 = find(indC11==14);
findInd_72_74_76 = [findInd_72_74_76 find(indC11==31)];
findInd_72_74_76 = [findInd_72_74_76 find(indC11==49)];
numfr_72_74_76 = zeros(size(findInd_72_74_76));
for i=1:length(findInd_72_74_76)
    [val, ind] = min(findInd_72_74_76);
    findInd_72_74_76(ind) = [];
    numfr_72_74_76(i) = val;
end
clear findInd_72_74_76 findInd_3_5_7
% ������������ � ������ ��������, ������������ ��� X
speedNavSKAxeX = zeros(1,(length(numfr_3_5_7)+length(numfr_72_74_76)));
speedNavSK = zeros(3,(length(numfr_3_5_7)+length(numfr_72_74_76)));
for i=1:length(speedNavSK)
    if isempty(numfr_72_74_76)
        [val, ind] = min(numfr_3_5_7);
        speedNavSK(1,i)=formValue([comm_d1(val,4), comm_d1(val,3)],[1, 1],[16,16]);
        speedNavSK(2,i)=formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]);
        speedNavSK(3,i)=formValue([comm_d1(val,8), comm_d1(val,7)],[1, 1],[16,16]);
        speedNavSKAxeX(i)=val*0.01;
        numfr_3_5_7(ind)=[];
        continue
    end
    if isempty(numfr_3_5_7)
        [val, ind] = min(numfr_72_74_76);
        speedNavSK(1,i)=formValue([comm_d1(val,73), comm_d1(val,72)],[1, 1],[16,16]);
        speedNavSK(2,i)=formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]);
        speedNavSK(3,i)=formValue([comm_d1(val,77), comm_d1(val,76)],[1, 1],[16,16]);
        speedNavSKAxeX(i)=val*0.01;
        numfr_72_74_76(ind)=[];
        continue
    end
    if min(numfr_3_5_7)<min(numfr_72_74_76)
        [val, ind] = min(numfr_3_5_7);
        speedNavSK(1,i)=formValue([comm_d1(val,4), comm_d1(val,3)],[1, 1],[16,16]);
        speedNavSK(2,i)=formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]);
        speedNavSK(3,i)=formValue([comm_d1(val,8), comm_d1(val,7)],[1, 1],[16,16]);
        speedNavSKAxeX(i)=val*0.01;
        numfr_3_5_7(ind)=[];
    else
        [val, ind] = min(numfr_72_74_76);
        speedNavSK(1,i)=formValue([comm_d1(val,73), comm_d1(val,72)],[1, 1],[16,16]);
        speedNavSK(2,i)=formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]);
        speedNavSK(3,i)=formValue([comm_d1(val,77), comm_d1(val,76)],[1, 1],[16,16]);
        speedNavSKAxeX(i)=val*0.01;
        numfr_72_74_76(ind)=[];
    end
end
clear ind val numfr_3_5_7 numfr_72_74_76
speedNavSK(1,:)=medfilt1(getN2C(speedNavSK(1,:),32),3);
speedNavSK(2,:)=medfilt1(getN2C(speedNavSK(2,:),32),3);
speedNavSK(3,:)=medfilt1(getN2C(speedNavSK(3,:),32),3);
figure('Name', '������������ �������� �������� � �����');
plot(speedNavSKAxeX,speedNavSK(1,:),speedNavSKAxeX,speedNavSK(2,:),...
    speedNavSKAxeX,speedNavSK(3,:),'LineWidth',2);
title('������������ �������� �������� � �����');xlabel('�����,�');ylabel('speedNavSK');
T = table(speedNavSK(1,:)',speedNavSK(2,:)',speedNavSK(3,:)',...
    speedNavSKAxeX','VariableNames',{'speedXnavSK' 'speedYnavSK' 'speedZnavSK' 'time'});
writetable(T,xlsFname,'Sheet','speedNavSK');
clear T

%% ������������ �������� �������� � ��������� ����������� ��
speedNGrSK = zeros(size(speedNavSK));
for i=1:length(speedNGrSK(1,:))
    speedNGrSK(:,i) = Mngr_nav*speedNavSK(:,i);
end
figure('Name', '������������ �������� �������� � �����');
plot(speedNavSKAxeX,speedNGrSK(1,:),speedNavSKAxeX,speedNGrSK(2,:),...
    speedNavSKAxeX,speedNGrSK(3,:),'LineWidth',2);
title('������������ �������� �������� � �����');xlabel('�����,�');ylabel('speedNGrSK');
T = table(speedNGrSK(1,:)',speedNGrSK(2,:)',speedNGrSK(3,:)',...
    speedNavSKAxeX','VariableNames',{'speedXNGrSK' 'speedYNGrSK' 'speedZNGrSK' 'time'});
writetable(T,xlsFname,'Sheet','speedNGrSK');
clear T

%% ������� ���������� ����� ������ �� ��������� ����� ������������
findInd_3 = find(indC11==18);
findInd_72 = find(indC11==44);
numfr_3 = zeros(1,length(findInd_3));
numfr_72 = zeros(1,length(findInd_72));
for i=1:length(findInd_3)
    [val, ind] = min(findInd_3);
    findInd_3(ind) = [];
    numfr_3(i) = val;
end
for i=1:length(findInd_72)
    [val, ind] = min(findInd_72);
    findInd_72(ind) = [];
    numfr_72(i) = val;
end
clear findInd_72 findInd_3
timeToPointAiming = zeros(1,(length(numfr_3)+length(numfr_72)));
timeToPointAimingTime = zeros(1,length(timeToPointAiming));
for i=1:length(timeToPointAiming)
    if isempty(numfr_72)
        [val, ind] = min(numfr_3);
        timeToPointAiming(i)=getFPD(comm_d1(val,4),formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]));
        timeToPointAimingTime(i)=val*0.01;
        numfr_3(ind)=[];
        continue
    end
    if isempty(numfr_3)
        [val, ind] = min(numfr_72);
        timeToPointAiming(i)=getFPD(comm_d1(val,73),formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]));
        timeToPointAimingTime(i)=val*0.01;
        numfr_72(ind)=[];
        continue
    end
    if min(numfr_3)<min(numfr_72)
        [val, ind] = min(numfr_3);
        timeToPointAiming(i)=getFPD(comm_d1(val,4),formValue([comm_d1(val,6), comm_d1(val,5)],[1, 1],[16,16]));
        timeToPointAimingTime(i)=val*0.01;
        numfr_3(ind)=[];
    else
        [val, ind] = min(numfr_72);
        timeToPointAiming(i)=getFPD(comm_d1(val,73),formValue([comm_d1(val,75), comm_d1(val,74)],[1, 1],[16,16]));
        timeToPointAimingTime(i)=val*0.01;
        numfr_72(ind)=[];
    end
end
clear numfr_3 numfr_72
figure('Name', '������� ���������� ����� ������ �� ��������� ����� ������������');
plot(timeToPointAimingTime,timeToPointAiming,'LineWidth',2);
title('������� ���������� ����� ������ �� ��������� ����� ������������');
xlabel('�����,�');ylabel('timeToPointAiming');

%% ����������� ���������� ������� ���� ������������ ���� A0, A1, A2 (����������� ��������)
orntVktrTyagi=zeros(3,length(comm_d1(:,15)));
orntVktrTyagi(1,:) = medfilt1(getN2C(comm_d1(:,15),16),3);
orntVktrTyagi(2,:) = medfilt1(getN2C(comm_d1(:,16),16),3);
orntVktrTyagi(3,:) = medfilt1(getN2C(comm_d1(:,17),16),3);
figure('Name', '����������� ���������� ������� ���� ������������ ���� A0, A1, A2');
plot(axeX100_D,orntVktrTyagi(1,:),axeX100_D,orntVktrTyagi(2,:),axeX100_D,orntVktrTyagi(3,:),'LineWidth',2);
title('����������� ���������� ������� ���� ������������ ���� A0, A1, A2');
xlabel('�����,�');ylabel('orntVktrTyagi');
T = table(orntVktrTyagi(1,:)',orntVktrTyagi(2,:)',orntVktrTyagi(3,:)',...
    axeX100_D','VariableNames',{'orntVktrTyagiA0' 'orntVktrTyagiA1' 'orntVktrTyagiA2' 'time'});
writetable(T,xlsFname,'Sheet','orntVktrTyagi');
clear T

%% ���� ��������
angleVystav = 90-(acos(orntVktrTyagi(1,:)./16384))*180/pi;
figure('Name', '���� ��������');
plot(axeX100_D,angleVystav,'LineWidth',2);
title('���� ��������');xlabel('�����,�');ylabel('angleVystav');
writetable(table(angleVystav',axeX100_D','VariableNames',{'UgolVystavki' 'time'}),xlsFname,'Sheet','UgolVystavki');

%% ������� �������� ������������ ���� X,Y,Z ��������� �� 
uglSpeed = zeros(3,length(comm_d4(:,45)));
uglSpeed(1,:) = medfilt1(getN2C(comm_d4(:,45),16),3);
uglSpeed(2,:) = medfilt1(getN2C(comm_d4(:,47),16),3);
uglSpeed(3,:) = medfilt1(getN2C(comm_d4(:,48),16),3);
figure('Name', '������� �������� ������������ ���� X,Y,Z ����');
plot(axeX100_D,uglSpeed(1,:),axeX100_D,uglSpeed(2,:),axeX100_D,uglSpeed(3,:),'LineWidth',2);
title('������� �������� ������������ ���� X,Y,Z ����');xlabel('�����,�');ylabel('uglSpeed');
T = table(uglSpeed(1,:)',uglSpeed(2,:)',uglSpeed(3,:)',...
    axeX100_D','VariableNames',{'uglSpeedX' 'uglSpeedY' 'uglSpeedZ' 'time'});
writetable(T,xlsFname,'Sheet','uglSpeed');
clear T

%% ������� �������� ������������ ���� X,Y,Z ��������� �� #2
uglSpeed_2 = zeros(3,length(comm_d4(:,45)));
uglSpeed_2(1,:) = medfilt1(getN2C(comm_d4(:,124),16),3);
uglSpeed_2(2,:) = medfilt1(getN2C(comm_d4(:,125),16),3);
uglSpeed_2(3,:) = medfilt1(getN2C(comm_d4(:,152),16),3);
figure('Name', '������� �������� ������������ ���� X,Y,Z ���� #2');
plot(axeX100_D,uglSpeed_2(1,:),axeX100_D,uglSpeed_2(2,:),axeX100_D,uglSpeed_2(3,:),'LineWidth',2);
title('������� �������� ������������ ���� X,Y,Z ���� #2');xlabel('�����,�');ylabel('uglSpeed_2');
clear T

%% ��������� �������������� ������ �� ���
sumCharactDuAbr = zeros(16,length(comm_d4(:,3)),'uint8');
for i = 1:length(comm_d4(:,3))
    for j=1:16
        sumCharactDuAbr(j,i) = formValue(comm_d4(i,3),(17-j),1);
    end
end
figure('Name', '��������� �������������� ������ �� ���');
subplot(4,4,1);plot(axeX100_D,sumCharactDuAbr(1,:),'LineWidth',2);title('�� ��� ����� 1');xlabel('�����,�');ylabel('');
subplot(4,4,2);plot(axeX100_D,sumCharactDuAbr(2,:),'LineWidth',2);title('�� ��� ����� 2');xlabel('�����,�');ylabel('');
subplot(4,4,3);plot(axeX100_D,sumCharactDuAbr(3,:),'LineWidth',2);title('�� ��� ����� 3');xlabel('�����,�');ylabel('');
subplot(4,4,4);plot(axeX100_D,sumCharactDuAbr(4,:),'LineWidth',2);title('�� ��� ����� 4');xlabel('�����,�');ylabel('');
subplot(4,4,5);plot(axeX100_D,sumCharactDuAbr(5,:),'LineWidth',2);title('�� ��� ����� 5');xlabel('�����,�');ylabel('');
subplot(4,4,6);plot(axeX100_D,sumCharactDuAbr(6,:),'LineWidth',2);title('�� ��� ����� 6');xlabel('�����,�');ylabel('');
subplot(4,4,7);plot(axeX100_D,sumCharactDuAbr(7,:),'LineWidth',2);title('�� ��� ����� 7');xlabel('�����,�');ylabel('');
subplot(4,4,8);plot(axeX100_D,sumCharactDuAbr(8,:),'LineWidth',2);title('�� ��� ����� 8');xlabel('�����,�');ylabel('');
subplot(4,4,9);plot(axeX100_D,sumCharactDuAbr(9,:),'LineWidth',2);title('�� ��� ����� 9');xlabel('�����,�');ylabel('');
subplot(4,4,10);plot(axeX100_D,sumCharactDuAbr(10,:),'LineWidth',2);title('�� ��� ����� 10');xlabel('�����,�');ylabel('');
subplot(4,4,11);plot(axeX100_D,sumCharactDuAbr(11,:),'LineWidth',2);title('�� ��� ����� 11');xlabel('�����,�');ylabel('');
subplot(4,4,12);plot(axeX100_D,sumCharactDuAbr(12,:),'LineWidth',2);title('�� ��� ����� 12');xlabel('�����,�');ylabel('');
subplot(4,4,13);plot(axeX100_D,sumCharactDuAbr(13,:),'LineWidth',2);title('�� ��� ����� 13');xlabel('�����,�');ylabel('');
subplot(4,4,14);plot(axeX100_D,sumCharactDuAbr(14,:),'LineWidth',2);title('�� ��� ����� 14');xlabel('�����,�');ylabel('');
subplot(4,4,15);plot(axeX100_D,sumCharactDuAbr(15,:),'LineWidth',2);title('�� ��� ����� 15');xlabel('�����,�');ylabel('');
subplot(4,4,16);plot(axeX100_D,sumCharactDuAbr(16,:),'LineWidth',2);title('�� ��� ����� 16');xlabel('�����,�');ylabel('');
T = table(sumCharactDuAbr(1,:)',sumCharactDuAbr(2,:)',sumCharactDuAbr(3,:)',...
    sumCharactDuAbr(4,:)',sumCharactDuAbr(5,:)',sumCharactDuAbr(6,:)',...
    sumCharactDuAbr(7,:)',sumCharactDuAbr(8,:)',sumCharactDuAbr(9,:)',...
    sumCharactDuAbr(10,:)',sumCharactDuAbr(11,:)',sumCharactDuAbr(12,:)',...
    sumCharactDuAbr(13,:)',sumCharactDuAbr(14,:)',sumCharactDuAbr(15,:)',...
     sumCharactDuAbr(16,:)',axeX100_D','VariableNames',...
     {'soplo1' 'soplo2' 'soplo3' 'soplo4' 'soplo5' 'soplo6' 'soplo7' 'soplo8' ...
     'soplo9' 'soplo10' 'soplo11' 'soplo12' 'soplo13' 'soplo14' 'soplo15' 'soplo16' 'time'});
writetable(T,xlsFname,'Sheet','sumCharactDuAbr');
clear T

%% ������� �� ��������� ��
kommandsOtd = zeros(12,length(comm_da(:,124)));
for i = 1:length(comm_da(:,124))
    for j=1:8
        kommandsOtd(j,i) = formValue(comm_da(i,124),(9-j),1);
    end
    for j=9:12
        kommandsOtd(j,i) = formValue(comm_da(i,136),(13-j),1);
    end
end
figure('Name', '������� �� ��������� ��');
subplot(3,4,1);plot(axeX100_D,kommandsOtd(1,:),'LineWidth',2);title('����� 1');xlabel('�����,�');ylabel('');
subplot(3,4,2);plot(axeX100_D,kommandsOtd(2,:),'LineWidth',2);title('����� 2');xlabel('�����,�');ylabel('');
subplot(3,4,3);plot(axeX100_D,kommandsOtd(3,:),'LineWidth',2);title('����� 3');xlabel('�����,�');ylabel('');
subplot(3,4,4);plot(axeX100_D,kommandsOtd(4,:),'LineWidth',2);title('����� 4');xlabel('�����,�');ylabel('');
subplot(3,4,5);plot(axeX100_D,kommandsOtd(5,:),'LineWidth',2);title('����� 5');xlabel('�����,�');ylabel('');
subplot(3,4,6);plot(axeX100_D,kommandsOtd(6,:),'LineWidth',2);title('����� 6');xlabel('�����,�');ylabel('');
subplot(3,4,7);plot(axeX100_D,kommandsOtd(7,:),'LineWidth',2);title('����� 7');xlabel('�����,�');ylabel('');
subplot(3,4,8);plot(axeX100_D,kommandsOtd(8,:),'LineWidth',2);title('����� 8');xlabel('�����,�');ylabel('');
subplot(3,4,9);plot(axeX100_D,kommandsOtd(9,:),'LineWidth',2);title('����� 9');xlabel('�����,�');ylabel('');
subplot(3,4,10);plot(axeX100_D,kommandsOtd(10,:),'LineWidth',2);title('����� 10');xlabel('�����,�');ylabel('');
subplot(3,4,11);plot(axeX100_D,kommandsOtd(11,:),'LineWidth',2);title('����� 11');xlabel('�����,�');ylabel('');
subplot(3,4,12);plot(axeX100_D,kommandsOtd(12,:),'LineWidth',2);title('����� 12');xlabel('�����,�');ylabel('');

%% ������� ��������� ��
momentsOtd = zeros(12,length(comm_da(:,136)));
for i = 1:length(comm_da(:,136))
    for j=1:4
        momentsOtd(j,i) = formValue(comm_da(i,136),(9-j),1);
    end
    for j=5:12
        momentsOtd(j,i) = formValue(comm_da(i,147),(13-j),1);
    end
end
figure('Name', '������� ��������� ��');
subplot(3,4,1);plot(axeX100_D,momentsOtd(1,:),'LineWidth',2);title('����� 1');xlabel('�����,�');ylabel('');
subplot(3,4,2);plot(axeX100_D,momentsOtd(2,:),'LineWidth',2);title('����� 2');xlabel('�����,�');ylabel('');
subplot(3,4,3);plot(axeX100_D,momentsOtd(3,:),'LineWidth',2);title('����� 3');xlabel('�����,�');ylabel('');
subplot(3,4,4);plot(axeX100_D,momentsOtd(4,:),'LineWidth',2);title('����� 4');xlabel('�����,�');ylabel('');
subplot(3,4,5);plot(axeX100_D,momentsOtd(5,:),'LineWidth',2);title('����� 5');xlabel('�����,�');ylabel('');
subplot(3,4,6);plot(axeX100_D,momentsOtd(6,:),'LineWidth',2);title('����� 6');xlabel('�����,�');ylabel('');
subplot(3,4,7);plot(axeX100_D,momentsOtd(7,:),'LineWidth',2);title('����� 7');xlabel('�����,�');ylabel('');
subplot(3,4,8);plot(axeX100_D,momentsOtd(8,:),'LineWidth',2);title('����� 8');xlabel('�����,�');ylabel('');
subplot(3,4,9);plot(axeX100_D,momentsOtd(9,:),'LineWidth',2);title('����� 9');xlabel('�����,�');ylabel('');
subplot(3,4,10);plot(axeX100_D,momentsOtd(10,:),'LineWidth',2);title('����� 10');xlabel('�����,�');ylabel('');
subplot(3,4,11);plot(axeX100_D,momentsOtd(11,:),'LineWidth',2);title('����� 11');xlabel('�����,�');ylabel('');
subplot(3,4,12);plot(axeX100_D,momentsOtd(12,:),'LineWidth',2);title('����� 12');xlabel('�����,�');ylabel('');

%% ���������� ����������
prodolPeregr = zeros(10,length(GTS_Aline(:,1)));
prodolPeregr(1,:) = medfilt1(GTS_Aline(:,125),3);
prodolPeregr(2,:) = medfilt1(GTS_Aline(:,126),3);
prodolPeregr(3,:) = medfilt1(GTS_Aline(:,128),3);
prodolPeregr(4,:) = medfilt1(GTS_Aline(:,129),3);
prodolPeregr(5,:) = medfilt1(GTS_Aline(:,138),3);
prodolPeregr(6,:) = medfilt1(GTS_Aline(:,139),3);
prodolPeregr(7,:) = medfilt1(GTS_Aline(:,141),3);
prodolPeregr(8,:) = medfilt1(GTS_Aline(:,142),3);
prodolPeregr(9,:) = medfilt1(GTS_Aline(:,158),3);
prodolPeregr(10,:) = medfilt1(GTS_Aline(:,159),3);
figure('Name', '���������� ����������');
subplot(3,4,1);plot(axeX400_A,prodolPeregr(1,:),'LineWidth',2);title('����� 1');xlabel('�����,�');ylabel('');
subplot(3,4,2);plot(axeX400_A,prodolPeregr(2,:),'LineWidth',2);title('����� 2');xlabel('�����,�');ylabel('');
subplot(3,4,3);plot(axeX400_A,prodolPeregr(3,:),'LineWidth',2);title('����� 3');xlabel('�����,�');ylabel('');
subplot(3,4,4);plot(axeX400_A,prodolPeregr(4,:),'LineWidth',2);title('����� 4');xlabel('�����,�');ylabel('');
subplot(3,4,5);plot(axeX400_A,prodolPeregr(5,:),'LineWidth',2);title('����� 5');xlabel('�����,�');ylabel('');
subplot(3,4,6);plot(axeX400_A,prodolPeregr(6,:),'LineWidth',2);title('����� 6');xlabel('�����,�');ylabel('');
subplot(3,4,7);plot(axeX400_A,prodolPeregr(7,:),'LineWidth',2);title('����� 7');xlabel('�����,�');ylabel('');
subplot(3,4,8);plot(axeX400_A,prodolPeregr(8,:),'LineWidth',2);title('����� 8');xlabel('�����,�');ylabel('');
subplot(3,4,9);plot(axeX400_A,prodolPeregr(9,:),'LineWidth',2);title('����� 9');xlabel('�����,�');ylabel('');
subplot(3,4,10);plot(axeX400_A,prodolPeregr(10,:),'LineWidth',2);title('����� 10');xlabel('�����,�');ylabel('');
T = table(prodolPeregr(1,:)',prodolPeregr(2,:)',prodolPeregr(3,:)',...
    prodolPeregr(4,:)',prodolPeregr(5,:)',prodolPeregr(6,:)',...
    prodolPeregr(7,:)',prodolPeregr(8,:)',prodolPeregr(9,:)',...
    prodolPeregr(10,:)',axeX400_A','VariableNames',...
     {'kanal1' 'kanal2' 'kanal3' 'kanal4' 'kanal5' 'kanal6' 'kanal7' 'kanal8' ...
     'kanal9' 'kanal10' 'time'});
writetable(T,xlsFname,'Sheet','prodolPeregr');
clear T

%% �������� � ������� �������� ��������
davlCamSgor = zeros(3,length(GTS_Aline(:,1)));
davlCamSgor(1,:) = 256-medfilt1(GTS_Aline(:,336),3);
davlCamSgor(2,:) = medfilt1(GTS_Aline(:,324),3);
davlCamSgor(3,:) = medfilt1(GTS_Aline(:,322),3);
figure('Name', '�������� � ������� �������� ��������');
plot(axeX400_A,davlCamSgor(1,:),axeX400_A,davlCamSgor(2,:),axeX400_A,davlCamSgor(3,:),...
    'LineWidth',2);title('�������� � ������� �������� ��������');xlabel('�����,�');ylabel('P');
davlCamSgorSvod(mode_A==0) = medfilt1(GTS_Aline(mode_A==0,336),3);
davlCamSgorSvod(mode_A==1) = medfilt1(GTS_Aline(mode_A==1,324),3);
davlCamSgorSvod(mode_A>=3) = medfilt1(GTS_Aline(mode_A>=3,322),3);
figure('Name', '������� �������� � ������� �������� ��������');
plot(axeX400_A,(256-davlCamSgorSvod),'LineWidth',2);
title('������� �������� � ������� �������� ��������');xlabel('�����,�');ylabel('P');
writetable(table(davlCamSgorSvod',axeX400_A','VariableNames', {'PcamSgor' 'time'}),...
    xlsFname,'Sheet','davlCamSgorSvod');

%% �������� � ���������� ��1
P_GG1=zeros(1,length(comm_d4(:,2)));
for i=1:length(comm_d4(:,2))
    P_GG1(i) = formValue(comm_d4(i,2),7,10);
end
figure('Name', '�������� � ���������� ��1');
plot(axeX100_D,P_GG1,'LineWidth',2);
title('�������� � ���������� ��1');xlabel('�����,�');ylabel('P');
writetable(table(P_GG1',axeX100_D','VariableNames', {'P_GG1' 'time'}),...
    xlsFname,'Sheet','P_GG1');

%% �������� � ���������� ��2
P_GG2 = GTS_Aline(:,87);


%% ��������� �������������� �������� � ���������������
sumP_GG = medfilt1(comm_d4(:,1),3);
sumP_GG(1:find(mode_D>3,1)) = 0;
figure('Name', '��������� �������������� �������� � ���������������');
plot(axeX100_D,sumP_GG,'LineWidth',2);
title('��������� �������������� �������� � ���������������');xlabel('�����,�');ylabel('P');
writetable(table(sumP_GG,axeX100_D','VariableNames',{'sumP_GG' 'time'}),xlsFname,'Sheet','sumP_GG');

%% 
save([fpath 'TMP.mat'])
disp('Decommutation complete.')