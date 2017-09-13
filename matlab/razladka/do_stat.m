function p = do_stat(DataIsh,frame_len,porog)
%начальные переменные
%размер скользящего окна (500)
%porog = 65;

koef = 10;
shag_sdvig = 1;
mascht = 30;

kol_vo_povtor = 1;
chast_kadr = 100;
shag_vrem = 1/(kol_vo_povtor * chast_kadr);
i_vyvod = 1;
Razm_min = frame_len/koef;
Sdvig = Razm_min*shag_sdvig;%шаг сдвига скользящего окна
sigsize = size(DataIsh);

count = fix((sigsize - frame_len)./Sdvig);
Mat_Oj = zeros(count(1, 1), 1);
Mat_Oj_min = zeros(count(1, 1), 1);
Sko = zeros(count(1, 1), 1);
Pravd = zeros(count(1, 1), 1);
Summa = zeros(count(1, 1), 1);
Win = zeros(frame_len, 1);
Win_min = zeros(Razm_min, 1);

for i = 1:1:(count(1, 1))
    Win = DataIsh((1 + (i - 1)*Sdvig):((i - 1)*Sdvig+frame_len));
    Win_min = Win((frame_len - Razm_min + 1): frame_len);
    Mat_Oj(i) = mean(Win);
    Mat_Oj_min(i) = mean(Win_min);
    Sko(i) = std(Win);
    if (i < 5) 
        Pravd(i) = 0;
    elseif (i > 5)
        Summa(i) = sum(Win_min - Mat_Oj(i) - (Mat_Oj_min(i) - Mat_Oj(i))/2);
        if (Sko(i) == 0)
            Sko(i) = .000001;
        end
        Pravd(i) = ((Mat_Oj_min(i) - Mat_Oj(i))/(Sko(i)^2)) * Summa(i);
        if (Pravd(i) < porog)
            Pravd(i) = 0;
        else
            vyvod(i_vyvod, 1) = ((i*(shag_vrem*Sdvig)) + ((frame_len - Razm_min)*shag_vrem) - shag_vrem*Sdvig);
            vyvod(i_vyvod, 2) = Pravd(i);
            i_vyvod = i_vyvod +1;
        end
    end
       
end

%t_x_MO = 0:(shag_vrem*Sdvig):(count(1,1)*Sdvig*shag_vrem)-shag_vrem;
%t_x_ish = 0:shag_vrem:(sigsize*shag_vrem)-shag_vrem;
t_x_pravd = ((frame_len - Razm_min)*shag_vrem):(shag_vrem*Sdvig):((count(1,1)*Sdvig*shag_vrem) + (frame_len - Razm_min)*shag_vrem - shag_vrem);
p.index = find(Pravd);
p.time = t_x_pravd(p.index);

end
