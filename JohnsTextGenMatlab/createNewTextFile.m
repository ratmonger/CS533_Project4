function textOutArray = createNewTextFile(td,sortedFwfdStruct,seedWord,outSz)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

    % numTdEnt = numEntries(td);
    % [~,fwfdSz] = size(sortedFwfdStruct);
    currWord = seedWord;
    % nextWord = "";
    textOutArray = strings(outSz,1);
    textOutArray(1) = currWord;

    for wrdNum = 1:outSz-1
        wordIdx = lookup(td,textOutArray(wrdNum));
        nextWord = chooseNextWord(sortedFwfdStruct{wordIdx});
        textOutArray(wrdNum+1) = nextWord;  
    end
end


function nextWord = chooseNextWord(sorteddicStruct)

    structSz = numel(fieldnames(sorteddicStruct));
    rnd = rand();
    for i = 1:structSz
       if sorteddicStruct(i).Value > rnd
           break;
       end
    end
    nextWord = sorteddicStruct(i).Key;
    
    % disp(nextWord);
   
end