path = uigetdir('');
if path == 0
    return
end
path = [path,'\'];
fmask = [path,'*.bit'];
files = dir(fmask);
if size(files,1)==0 
    return
end

porogs = 20:20:220;
frames = [200 500 1000];

%ft = inputdlg({'Decode mode (0-UnQuantized, 1-Quantized):','Frame types: 0-All, 1-I, 2-P, 3-B'},'Frame type',1,{'1','1'});

cyclo_times = dlmread('cyclogramma.txt');
%disp(cyclo_times);

mkdir('test_result');
log_fid = fopen('./test_result/result.txt','w');
% fid_stego = fopen('./result_cmplx/stego_cmplx.dat','wb');

%14.D4

for nfile=1:1:size(files,1)

    disp(files(nfile).name)
    fprintf(log_fid,'\n%s\n',files(nfile).name);
    
    infile = fopen([path,files(nfile).name],'r');
    %чтение массива данных
    DataIsh = fread(infile, 'int16');
    fclose(infile);
    
    for pp=1:1:size(porogs,2)
        for fs=1:1:size(frames,2)
            r = do_stat(DataIsh, frames(fs), porogs(pp));
            %disp(r)
            zz = zeros(size(r.time));
            for i=1:1:size(cyclo_times,1)
                zz = zz | ((r.time > (cyclo_times(i) - 0.25))&(r.time < (cyclo_times(i) + 0.25)));
            end
            sovp_cnt = size(r.time(zz),2);
    
            err1 = (size(cyclo_times,1) - sovp_cnt)/size(cyclo_times,1);
            err2 = (size(r.time,2) - sovp_cnt)/size(r.time,2); 
            
            str = sprintf('пиков: %d, совпадений: %d\nпропуск: %d, ложна€ тревога: %d', size(zz,2),sovp_cnt,err1,err2);
            fprintf(log_fid,'ѕорог: %d, окно: %d\n',porogs(pp), frames(fs));
            fprintf(log_fid,'%s\n',str);
            fprintf(log_fid,'%f\n',r.time(zz)');
    
            %disp(str)
            %disp(r.time(zz)')
    
        end %frame_size
    end %porogs
end
fclose(log_fid);
% fclose(fid_stego);


