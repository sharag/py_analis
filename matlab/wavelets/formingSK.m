%% Скачки
function SKstruct = formingSK(sizeOfSk)
    % sizeOfSk = 1000;
    
    % единичный скачок
    skEd = zeros(1, sizeOfSk);
    skEd(floor(sizeOfSk/2):sizeOfSk) = 1;
    skEd_norm = (skEd-0.5)*2;
    skEd_ = 1-skEd;
    skEd_norm_ = (skEd_-0.5)*2;

    
     
    
    
    
    % Полоса
    skStripe = zeros(1, sizeOfSk);
    step = floor(sizeOfSk/10);
    skStripe(step*4:step*6) = 1;
    skStripeObr = 1-skStripe;
    skStripe_0 = (skStripe-0.5)*2;
    skStripeObr_0 = 1-skStripe_0;
    skStripe_1 = zeros(1, sizeOfSk);
    skStripe_1(step*2:step*4)=-1;skStripe_1(step*4:step*6)=1;skStripe_1(step*6:step*8)=-1;
    skStripeObr_1 = 1-skStripe_1;
    clear step
    % Пирамида
    skPiramid = zeros(1,sizeOfSk);
    stepX = floor(sizeOfSk/3);
    stepY = 1/(stepX/2);
    for i = stepX:(stepX+floor(stepX/2))
        skPiramid(i) = (i-stepX)*stepY;
    end
    for i = (stepX+floor(stepX/2)):stepX*2
        skPiramid(i) = 1-(i-(stepX+floor(stepX/2)))*stepY;
    end
    clear stepX stepY i
    
    skPiramidObr = 1-skPiramid;

    % Синусоида
    skSin = zeros(1,sizeOfSk);
    step = floor(sizeOfSk/3);
    for i = step:1:step*2
        skSin(i) = sin((i-step)/10);
    end
    clear i step

    skSinObr = 1-skSin;

    % Парабола
    skParab = zeros(1,sizeOfSk);
    step = floor(sizeOfSk/3);
    max = step^2;
    for i = step:1:step*2
        skParab(i) = (i-step)^2/max;
    end
    skParab(step*2:sizeOfSk) = 1;
    clear step i max

    skParabObr = 1 - skParab;

    % Гипербола
    skGiperb = zeros(1,sizeOfSk);
    step = floor(sizeOfSk/3);
    max = step^3;
    for i = step:1:step*2
        skGiperb(i) = (i-step)^3/max;
    end
    skGiperb(step*2:sizeOfSk) = 1;
    clear step i max

    skGiperbObr = 1 - skGiperb;

    % sinc
    skSinc = zeros(1, sizeOfSk);
    step = floor(sizeOfSk/3);
    for i = step:1:step*2
        skSinc(i) = sinc((i-step-step/2)/10);
    end
    clear i step

    skSincObr = 1-skSinc;
    
    SKstruct = struct('skEd',skEd,'skEdObr',skEd_,'skEd_0',skEd_norm,...
        'skEdObr_0',skEd_norm_,'skStripe',skStripe,...
        'skStripeObr',skStripeObr,'skPiramid',skPiramid,...
        'skPiramidObr',skPiramidObr,'skParab',skParab,...
        'skParabObr',skParabObr,'skGiperb',skGiperb,...
        'skGiperbObr',skGiperbObr,'skSin',skSin,'skSinObr',skSinObr,...
        'skSinc',skSinc,'skSincObr',skSincObr);
end