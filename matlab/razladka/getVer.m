function [ numPO, numLT, numPC ] = getVer( s, sInd, koefPorog, numTest, Posh, num_s, numOrder, winBef, winAft)
%GETVER ������� �������� ������������� ������������� ����������� �������


% ������ ���������� ������� �� �� ����������� ������
numPO = zeros(size(Posh));
% ������ ���������� ������� �� �� ����������� ������
numLT = zeros(size(Posh));
% ������ ���������� ������� �� �� ����������� ������
numPC = zeros(size(Posh));
% ���������� �������� ����������� ������ �� ���
lenPosh = length(Posh);

% ��������� ������� �������� ������� �� �������
surgeInd = [];
cur_surge = 1;
indCurSurge = 1;
for i = 2:1:length(sInd)
    if sInd(i) - sInd(i - 1) > 1
        cur_surge = cur_surge + 1;
        indCurSurge = 1;
    else
        surgeInd(cur_surge, indCurSurge) = sInd(i);
        indCurSurge = indCurSurge + 1;
    end
end

% ���� �� ���������� �������� ����������� ������ �� ���
for pInd = 1:1:lenPosh
    disp(['���� (' num2str(pInd) ' / ' num2str(lenPosh) ')'])
    
    % ���� �� ���������� �������������
    for curTest = 1:1:numTest
        % ��������� �����
        sBad = s;
        numBadSample = floor(length(sBad) * Posh(pInd) + 0.5);
        badSamples = randi([1 length(sBad)], [1 numBadSample]);
        for iSample = 1:1:numBadSample
            badValueOrd = randi([0 numOrder], 1) + 1;
            if bitget(sBad(badSamples(iSample)), badValueOrd)
                sBad(badSamples(iSample)) = ...
                    bitset(sBad(badSamples(iSample)), badValueOrd, 0);
            else
                sBad(badSamples(iSample)) = ...
                    bitset(sBad(badSamples(iSample)), badValueOrd, 1);
            end
        end
        
        % ��������� ������� ��������� �������������
        probability__ = get_probability( sBad, winBef, winAft );
        % ����������
        maxProb = max(probability__);
        porog = koefPorog * maxProb;
        
        % ��������� ���������� �������� ��������� �������������
        % ���������� �������� � ���������� ��, ��, ��
        % ����� �������� �������� ���
        k = 1; % ����� �������� �������� ���
        % ���������� ������� �� ��� �������� �����
        numPOtest = 0;
        % ���������� ������� �� ��� �������� �����
        numLTtest = 0;
        % ���������� ������� �� ��� �������� �����
        numPCtest = 0;
        % ������ �������� ���, ����������� �����
        probInd = [];
        % ���������� ����� �������� ���, ������������ �����
        numProbInd = 0;
        % ��������� ���������� ������ �������� �������������
        while 1
            if k >= (length(probability__) - 1)
                break;
            end
            if probability__(k) < porog
                k = k + 1;
                continue;
            else % ������������ ������� �������� ��������
                % �������������, ����������� �����
                while probability__(k) > porog
                    if k >= (length(probability__) - 1)
                        break;
                    end
                    numProbInd = numProbInd + 1;
                    probInd(numProbInd) = k + winBef;
                    k = k + 1;
                end
            end
        end
        if isempty(probInd)
            numPC(pInd) = numPC(pInd) + num_s;
            break;
        end
        
        % ������� ������� ������������ �������� � ��������� ������ �
        % ���������� ���������� ������� ��, ��, ��
        statObn = [];
        for nSurge = 1:1:num_s
            nObnInd = 1;
            nObnSurge = 1;
            while 1
                for nSample = 1:1:size(surgeInd, 2)
                    statObn(nSurge, nObnSurge) = 0;
                    if isempty(probInd)
                        disp('11')
                    end
                    if probInd(nObnInd) == surgeInd(nSurge, nSample)
                        statObn(nSurge, nObnSurge) = 1;
                        break;
                    end
                end
                if length(probInd) == nObnInd
                    break
                end
                nObnInd = nObnInd + 1;
                if probInd(nObnInd) - probInd(nObnInd - 1) > 1
                    nObnSurge = nObnSurge + 1;
                end
            end
            
        end
        
        % ������ ������������ ������������ � �������� �������
        for i_s = 1:1:num_s
            obnSign = false;
            for i_p = 1:1:size(statObn, 2)
                if statObn(i_s, i_p)
                    if i_s == i_p
                        numPOtest = numPOtest + 1;
                        obnSign = true;
                    else
                        numLTtest = numLTtest + 1;
                    end
                end
            end
            if ~obnSign
                numPCtest = numPCtest + 1;
            end
        end
        numPC(pInd) = numPC(pInd) + numPCtest;
        numPO(pInd) = numPO(pInd) + numPOtest;
        numLT(pInd) = numLT(pInd) + numLTtest;
    end
    numPC(pInd) = numPC(pInd) ./ numTest ./ num_s;
    numPO(pInd) = numPO(pInd) ./ numTest ./ num_s;
    numLT(pInd) = numLT(pInd) ./ numTest ./ num_s;
end
end
