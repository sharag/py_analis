
function dataSinhr = formBitGTS(dataBit, lenFrame, lenSinhr, sinhraHEXstr, porogHem)
%lenFrame = 2880;
%lenSinhr = 24;
%porogHem = 3;
%sinhra = hexToBinaryVector('0x0db573', lenSinhr);
sinhra = hexToBinaryVector(sinhraHEXstr, lenSinhr);
dataSinhr = false(ceil(length(dataBit)/(lenFrame)), lenFrame);
GTS_Sign = true;
i = lenSinhr;
numFrame = 0;
lastBit = 0;
lossBitUp = 0;
lossBitDown = 0;
persentStep = fix(length(dataBit)/100);
lastPersent = 0;
while GTS_Sign
    % ���� ����� ��� ���������
    if (i + lenFrame) < (length(dataBit) - 1)
        % ���� ���������� �������� � �������
        if distHemBit(dataBit((i - lenSinhr + 1):i), sinhra) <= porogHem
            fromLastBit = abs(i - lenSinhr - lastBit);
            % ���� ���� ������
            if fromLastBit ~= 0
                % ���� ������ ������ �������� �����
                if round(fromLastBit/lenFrame)
                    for j = 1:1:round(fromLastBit/lenFrame)
                        dataSinhr((numFrame + 1), 1:lenFrame) = ...
                            dataSinhr(numFrame, 1:lenFrame);
                        numFrame = numFrame + 1;
                    end
                    disp(['��������� ������: ' num2str(round(fromLastBit/lenFrame))]);
                    fromLastBit = fromLastBit - round(fromLastBit/lenFrame)*lenFrame;
                    if (fromLastBit) > 0
                        lossBitUp = lossBitUp + fromLastBit;
                        disp(['��������� ' num2str(fromLastBit) ' ���']);
                    elseif (fromLastBit) < 0
                        lossBitDown = lossBitDown + abs(fromLastBit);
                        disp(['�������� ' num2str(abs(fromLastBit)) ' ���']);
                    end
                % ���� ������ ������ �������� �����
                else
                    if (fromLastBit) > 0
                        lossBitUp = lossBitUp + fromLastBit;
                        disp(['��������� ' num2str(fromLastBit) ' ���']);
                    else
                        lossBitDown = lossBitDown + abs(fromLastBit);
                        disp(['�������� ' num2str(abs(fromLastBit)) ' ���']);
                    end
                end
            end
            % ���������� ���
            dataSinhr((numFrame + 1), 1:lenSinhr) = ...
                sinhra(:);
            dataSinhr((numFrame + 1), (lenSinhr + 1):lenFrame) = ...
                dataBit((i + 1):(i - lenSinhr + lenFrame));
            numFrame = numFrame + 1;
            lastBit = i + lenFrame - lenSinhr;
            i = i + lenFrame - lenSinhr;
        % ���������� �������� ��� �������
        else
            i = i + 1;
        end 
    % ���� ��� ���������� - �����
    else 
        GTS_Sign = false;
        break;
    end
    if (i/persentStep - lastPersent) > 0.1
        lastPersent = i/persentStep;
        disp([num2str(i/persentStep), ' %']);
    end
end
dataSinhr((numFrame+1):end,:) = [];
end