clc 
clear
[fname, fpath] = uigetfile('*.bit','Выберите файл ГТС A-линии','E:\MATscripts\');%
if isequal(fname, 0)
   disp('Выбор файла отменен.');
   return
else
   disp(['Выбран файл: ', fullfile(fpath, fname), '.']);
end
dataFID = fopen(fullfile(fpath, fname), 'r');
data = fread(dataFID,'uint8');
fclose(dataFID);
if (length(data) < 3)
    disp('Слишком маленький файл.');
    return
end
disp('Save raw data.')
save([fpath '__GTS_A.mat'])
disp('Save raw data complete.')
clear dataFID fname

sinhr = false;
numFrame = 0;
passbyte = 0;
beg = 1;
lenFrame = 360;
porogHem = 3; 
sinhromarker = [176,173,206]; % маркер из 4-х слов до реверса в формате uint8
GTS_Aline = zeros(ceil(length(data)/lenFrame),lenFrame);
numword = 0;
for i = beg:(length(data)-(length(sinhromarker)-1))
    if sinhr == true
        numword = numword + 1;
        GTS_Aline(numFrame,numword) = revers(data(i),8);
    else
        if distHem(data(i:(i+(length(sinhromarker)-1))),8,sinhromarker,8) < porogHem
            sinhr = true;
            numFrame = numFrame +1;
            numword = numword + 1;
            GTS_Aline(numFrame,numword) = revers(data(i),8);
            continue
        else
            passbyte = passbyte + 1;
            disp(['Number of passed byte: ' num2str(passbyte)])
        end
    end
    if numword == lenFrame
        if rem(numFrame,100) == 0
            disp(['Progress: ' num2str(i/length(data)*100) '%, frame number: ' num2str(numFrame) '.']);
            if rem(numFrame,10000) == 0
                disp('Save data.')
                save([fpath '__GTS_A.mat'])
                disp('Save data complete.')
                beg = i;
            end
        end
        sinhr = false;
        numword = 0;
    end
end
GTS_Aline((numFrame+1):length(GTS_Aline),:) = [];
disp('Save data.')
save([fpath '__GTS_A.mat'])
disp('Save data complete.')
disp('Forming GTS A-line complete.')
disp('Save rezults.')
save([fpath 'GTS_A.mat'],'GTS_Aline','fpath')
disp('Save rezults complete.')
