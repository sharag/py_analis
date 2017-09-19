function [ numPO, numLT, numPC ] = getVer( s, sInd, koefPorog, numTest, Posh, num_s, numOrder, winBef, winAft)
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
        indCurSurge = indCurSurge + 1;
    end
end

% Цикл по количеству значений вероятности ошибки на бит
for pInd = 1:1:lenPosh
    disp(['Тест (' num2str(pInd) ' / ' num2str(lenPosh) ')'])
    
    % Цикл по количеству экспериментов
    for curTest = 1:1:numTest
        % Добавляем шумов
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
        
        % Вычисляем функцию отношения правдоподобия
        probability__ = get_probability( sBad, winBef, winAft );
        % Определяем
        maxProb = max(probability__);
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
            if k >= (length(probability__) - 1)
                break;
            end
            if probability__(k) < porog
                k = k + 1;
                continue;
            else % Подсчитываем индексы значений функциии
                % правдоподобия, превышающих порог
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
        
        % Сверяем индексы обнаруженных участков с индексами скачка и
        % определяем количество событий ПО, ЛТ, ПЦ
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
        
        % Оценка соответствия обнаруженных и реальных скачков
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
