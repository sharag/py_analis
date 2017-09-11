comm_d1 = zeros(length(GTS_Dline(:,1)),153);
comm_d3 = zeros(length(GTS_Dline(:,1)),153);
comm_d4 = zeros(length(GTS_Dline(:,1)),153);
comm_da = zeros(length(GTS_Dline(:,1)),300);

% D1, D3, D4, DA
for ifr = 1:1:length(GTS_Dline(:,1)) % по количеству кадров
    for iwrld = 0:1:152 % по кадру - 153 слова
        comm_d1(ifr,iwrld+1) = formValue([GTS_Dline(ifr,(6+iwrld*12));GTS_Dline(ifr,(5+iwrld*12))],[1;1],[8;8]);
        comm_d3(ifr,iwrld+1) = formValue([GTS_Dline(ifr,(10+iwrld*12));GTS_Dline(ifr,(9+iwrld*12))],[1;1],[8;8]);
        comm_d4(ifr,iwrld+1) = formValue([GTS_Dline(ifr,(12+iwrld*12));GTS_Dline(ifr,(11+iwrld*12))],[1;1],[8;8]);
    end
    for iwrld = 0:1:49 % по кадру - первые 100 слов
        comm_da(ifr,(iwrld*2 + 1)) = GTS_Dline(ifr,(15+iwrld*12));
        comm_da(ifr,(iwrld*2 + 2)) = GTS_Dline(ifr,(16+iwrld*12));
    end
    for iwrld = 50:1:99 % по кадру - вторые 100 слов
        comm_da(ifr,(iwrld*2 + 1)) = GTS_Dline(ifr,(27+iwrld*12));
        comm_da(ifr,(iwrld*2 + 2)) = GTS_Dline(ifr,(28+iwrld*12));
    end
    for iwrld = 100:1:149 % по кадру - третьи 100 слов
        comm_da(ifr,(iwrld*2 + 1)) = GTS_Dline(ifr,(39+iwrld*12));
        comm_da(ifr,(iwrld*2 + 2)) = GTS_Dline(ifr,(40+iwrld*12));
    end
    if rem(ifr,100) == 0
        disp(['Progress decommutation: ' num2str(ifr/length(GTS_Dline(:,1))*100) ...
            '%, frame number: ' num2str(ifr) '.']);
        if rem(ifr,10000) == 0
            disp('Save data.')
        	save([fpath '__GTS_D_comms.mat'])
            disp('Save data complete.')
        end
    end
end
disp('Save data.')
save([fpath '__GTS_D_comms.mat'])
disp('Save data complete.')
disp('Decommutation complete.')
disp('Save rezults.')
save([fpath 'GTS_D_comms.mat'], 'fpath', 'comm_d1', 'comm_d3', 'comm_d4', 'comm_da')
disp('Save rezults complete.')