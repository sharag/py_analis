function [ po, lt, pc ] = getVer( s, sInd, koefPorog, numTest, Posh, num_s, numOrder, winBef, winAft)
%GETVER Функция рассчета вероятностных характеристик обнаружения скачков


% Массив количества событий ПО от вероятности ошибки
numPO = zeros(size(Posh));
% Массив количества событий ЛТ от вероятности ошибки
numLT = zeros(size(Posh));
% Массив количества событий ПЦ от вероятности ошибки
numPC = zeros(size(Posh));
% Количество значений вероятности ошибки на бит
lenPosh = length(Posh);

% Разбиение массива индексов скачков по скачкам
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

% Цикл по количеству значений вероятности ошибки на бит
for pInd = 1:1:lenPosh
    disp(['Тест (' num2str(pInd) ' / ' num2str(lenPosh)])
    
    % Цикл по количеству экспериментов
    for curTest = 1:1:numTest
        % Добавляем шумов
        sBad = s;
        numBadSample = floor(length(sBad) * Posh(pInd) + 0.5);
        badSamples = randi([0 length(sBad)], [1 numBadSample]);
        badValues = randi([0 (2 ^ numOrder)], [1 numBadSample]);
        for iSample = 1:1:numBadSample
            sBad(badSamples(iSample)) = badValues(iSample);
        end
        
        % Вычисляем функцию отношения правдоподобия
        probability = get_probability( sBad, winBef, winAft );
        % Определяем 
        maxProb = max(probability);
        porog = koefPorog * maxProb;
        
        % Проверяем превышение функцией отношения правдоподобия
        % порогового значения и определяем ПО, ЛТ, ПЦ
        % Номер текущего значения ФОП
        k = 1; % Номер текущего значения ФОП
        % Количество событий ПО для текущего теста
        numPOtest = 0;
        % Количество событий ЛТ для текущего теста
        numLTtest = 0;
        % Количество событий ПЦ для текущего теста
        numPCtest = 0;
        % Массив индексов ФПО, превышающих порог
        probInd = [];
        % Порядковый номер значения ФПО, превысившего порог
        numProbInd = 0;
        % Проверяем превышение порога функцией правдоподобия
        while 1 
            if k >= (length(probability) - 1)
                break;
            end
            if probability(k) < porog
                k = k + 1;
                continue;
            else % Подсчитываем индексы значений функциии
                % правдоподобия, превышающих порог
                while probability(k) > porog
                    if k >= (length(probability) - 1)
                        break;
                    end
                    numProbInd = numProbInd + 1;
                    probInd(numProbInd) = k + winBef;
                    k = k + 1;
                end
                
                % Сверяем обнаруженные индексы с индексами скачка
                %obn = false;
                %                 obn = False
                %                 for ind in indexes_prob:
                %                     if ind in indexes_skach:
                %                         obn = True
                %                         break
                %                 # принимаем решение: обнаружение или ложная тревога
                %                 if obn:
                %                     num_po_test += 1
                %                 else:
                %                     num_lt_test += 1
                
            end
            
            % Сверяем индексы обнаруженных участков с индексами скачка и
            % определяем количество событий ПО, ЛТ, ПЦ
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
    %     num_po = 0  # Правильное обнаружение
    %     num_lt = 0  # Ложная тревога
    %     num_pc = 0  # Пропуск цели
    %     for i in range(num_test):  # Испытания
    %         signal = add_nois(insignal, p)
    %         prob = f_probability(signal, win_bef, win_aft)
    %         k = 0
    %         num_po_test = 0  # Правильное обнаружение
    %         num_lt_test = 0  # Ложная тревога
    %         num_pc_test = 0  # Пропуск цели
    %         while True:  # Проверяем превышение порога функцией правдоподобия
    %             if k >= (prob.size - 1):
    %                 break
    %             if prob[k] < porog:
    %                 k += 1
    %                 continue
    %             else:  # Подсчитываем индексы значений функциии правдоподобия, превышающих порог
    %                 indexes_prob = np.array([])
    %                 while prob[k] > porog:
    %                     if k >= (prob.size-1):
    %                         break
    %                     indexes_prob = np.append(indexes_prob, k + win_bef)
    %                     k += 1
    
    
    
    %                 # Сверяем обнаруженные индексы с индексами скачка
    %                 obn = False
    %                 for ind in indexes_prob:
    %                     if ind in indexes_skach:
    %                         obn = True
    %                         break
    %                 # принимаем решение: обнаружение или ложная тревога
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
