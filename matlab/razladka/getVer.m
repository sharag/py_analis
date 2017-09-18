function [ po, lt, pc ] = getVer( s, sInd, koefPorog, numTest, Posh, num_s, numOrder, winBef, winAft)
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
    end
end

% ���� �� ���������� �������� ����������� ������ �� ���
for pInd = 1:1:lenPosh
    disp(['���� (' num2str(pInd) ' / ' num2str(lenPosh)])
    
    % ���� �� ���������� �������������
    for curTest = 1:1:numTest
        % ��������� �����
        sBad = s;
        numBadSample = floor(length(sBad) * Posh(pInd) + 0.5);
        badSamples = randi([0 length(sBad)], [1 numBadSample]);
        badValues = randi([0 (2 ^ numOrder)], [1 numBadSample]);
        for iSample = 1:1:numBadSample
            sBad(badSamples(iSample)) = badValues(iSample);
        end
        
        % ��������� ������� ��������� �������������
        probability = get_probability( sBad, winBef, winAft );
        % ���������� 
        maxProb = max(probability);
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
            if k >= (length(probability) - 1)
                break;
            end
            if probability(k) < porog
                k = k + 1;
                continue;
            else % ������������ ������� �������� ��������
                % �������������, ����������� �����
                while probability(k) > porog
                    if k >= (length(probability) - 1)
                        break;
                    end
                    numProbInd = numProbInd + 1;
                    probInd(numProbInd) = k + winBef;
                    k = k + 1;
                end
                
                % ������� ������������ ������� � ��������� ������
                %obn = false;
                %                 obn = False
                %                 for ind in indexes_prob:
                %                     if ind in indexes_skach:
                %                         obn = True
                %                         break
                %                 # ��������� �������: ����������� ��� ������ �������
                %                 if obn:
                %                     num_po_test += 1
                %                 else:
                %                     num_lt_test += 1
                
            end
            
            % ������� ������� ������������ �������� � ��������� ������ �
            % ���������� ���������� ������� ��, ��, ��
            statObn = [];
            for nSurge = 1:1:size(surgeInd, 1)
                statObn(nSurge) = 0;
                nObnInd = 2;
                nObnSurge = 1;
                while 1
                    if probInd(nObnInd) - probInd(nObnInd - 1) > 1
                        nObnSurge = nObnSurge + 1;
                    end
                    for nSample = 1:1:size(surgeInd, 2)
                        if probInd(nObnInd) == surgeInd(nSurge, nSample)
                            statObn(nSurge) = statObn(nSurge) + 1;
                        end
                    end
                end
                
                    
                    
                    
                    
                    for nObnind = 1:1:length(probInd)
                        
                    end
                    
                end
            end
    %                 obn = False
    %                 for ind in indexes_prob:
    %                     if ind in indexes_skach:
    %                         obn = True
    %                         break
            
            
            
            
            
            
        end
    end
    
    
    
    
    num_po = np.append(num_po, num_po_)
    num_lt = np.append(num_lt, num_lt_)
    num_pc = np.append(num_pc, num_pc_)
    po_ = num_po/num_test/n_surge
    lt_ = num_lt/num_test/n_surge
    pc_ = num_pc/num_test/n_surge
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    %
    %
    %
    %
    %     num_po = 0  # ���������� �����������
    %     num_lt = 0  # ������ �������
    %     num_pc = 0  # ������� ����
    %     for i in range(num_test):  # ���������
    %         signal = add_nois(insignal, p)
    %         prob = f_probability(signal, win_bef, win_aft)
    %         k = 0
    %         num_po_test = 0  # ���������� �����������
    %         num_lt_test = 0  # ������ �������
    %         num_pc_test = 0  # ������� ����
    %         while True:  # ��������� ���������� ������ �������� �������������
    %             if k >= (prob.size - 1):
    %                 break
    %             if prob[k] < porog:
    %                 k += 1
    %                 continue
    %             else:  # ������������ ������� �������� �������� �������������, ����������� �����
    %                 indexes_prob = np.array([])
    %                 while prob[k] > porog:
    %                     if k >= (prob.size-1):
    %                         break
    %                     indexes_prob = np.append(indexes_prob, k + win_bef)
    %                     k += 1
    
    
    
    %                 # ������� ������������ ������� � ��������� ������
    %                 obn = False
    %                 for ind in indexes_prob:
    %                     if ind in indexes_skach:
    %                         obn = True
    %                         break
    %                 # ��������� �������: ����������� ��� ������ �������
    %                 if obn:
    %                     num_po_test += 1
    %                 else:
    %                     num_lt_test += 1
    %         if num_po_test < num_skach:
    %             num_pc_test = num_skach - num_po_test
    %         if num_po_test > num_skach:
    %             num_lt_test += num_po_test - num_skach
    %             num_po_test = num_skach
    %         num_po += num_po_test
    %         num_lt += num_lt_test
    %         num_pc += num_pc_test
    %     return num_po, num_lt, num_pc
    %
    %
end
end
