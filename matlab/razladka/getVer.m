function [ po, lt, pc ] = getVer( s, sInd, koefPorog, numTest, Posh, num_s, porog, numOrder, winBef, winAft)
%GETVER Функция рассчета вероятностных характеристик обнаружения скачков
    numPO = zeros(size(Posh));
    numLT = zeros(size(Posh));
    numPC = zeros(size(Posh));
    lenPosh = length(Posh);
    
    cur_surge = 1
    surgeInd = [][]
    for i = 2:1:length(sInd)
        if sInd(i) - sInd(i - 1) > 1
            
        else
            
        end
    end
    
    i = 0
    for pInd = 1:1:lenPosh
        i = i + 1;
        disp(['Тест (' num2str(i) ' / ' num2str(lenPosh)])
        % Добавляем шумов
        sBad = s;
        numBadSample = floor(length(sBad) * Posh(pInd) + 0.5);
        badSamples = randi([0 length(sBad)], [1 numBadSample]);
        badValues = randi([0 (2 ^ numOrder)], [1 numBadSample])
        for iSample = 1:1:numBadSample
            sBad(badSamples(iSample)) = badValues(iSample);
        end
        % Вычисляем функцию отношения правдоподобия 
        probability = get_probability( sBad, winBef, winAft );
        
        
        
        
        
        
        num_po = np.append(num_po, num_po_)
        num_lt = np.append(num_lt, num_lt_)
        num_pc = np.append(num_pc, num_pc_)
    po_ = num_po/num_test/n_surge
    lt_ = num_lt/num_test/n_surge
    pc_ = num_pc/num_test/n_surge
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    num_po = 0  # Правильное обнаружение
    num_lt = 0  # Ложная тревога
    num_pc = 0  # Пропуск цели
    for i in range(num_test):  # Испытания
        signal = add_nois(insignal, p)
        prob = f_probability(signal, win_bef, win_aft)
        k = 0
        num_po_test = 0  # Правильное обнаружение
        num_lt_test = 0  # Ложная тревога
        num_pc_test = 0  # Пропуск цели
        while True:  # Проверяем превышение порога функцией правдоподобия
            if k >= (prob.size - 1):
                break
            if prob[k] < porog:
                k += 1
                continue
            else:  # Подсчитываем индексы значений функциии правдоподобия, превышающих порог
                indexes_prob = np.array([])
                while prob[k] > porog:
                    if k >= (prob.size-1):
                        break
                    indexes_prob = np.append(indexes_prob, k + win_bef)
                    k += 1
                # Сверяем обнаруженные индексы с индексами скачка
                obn = False
                for ind in indexes_prob:
                    if ind in indexes_skach:
                        obn = True
                        break
                # принимаем решение: обнаружение или ложная тревога
                if obn:
                    num_po_test += 1
                else:
                    num_lt_test += 1
        if num_po_test < num_skach:
            num_pc_test = num_skach - num_po_test
        if num_po_test > num_skach:
            num_lt_test += num_po_test - num_skach
            num_po_test = num_skach
        num_po += num_po_test
        num_lt += num_lt_test
        num_pc += num_pc_test
    return num_po, num_lt, num_pc
    
    
end

