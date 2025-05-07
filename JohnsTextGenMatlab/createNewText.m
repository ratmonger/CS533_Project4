function newText = createNewText(d,wordDic,textArrayIn)

    [numWords,~] = size(textArrayIn);
    numEnt = d.numEntries;
        %Get total number of each work occurences
    for i = 1:numEnt
       totalArray(i) = sum(values(wordDic{i}));
    end
    for i = 1:numWords-1
        newText(i) = ChooseNextWord(d,textArrayIn(i),wordDic,totalArray);


    end




end


function nextWord = ChooseNextWord(d,currWord,wordDic,totalArray)
    
    sum(values(wordDic{lookup(d,currWord)}));
    currWrdDic = wordDic{lookup(d,currWord)};

    [val,idx] = max(values(currWrdDic{lookup(mdP1Dic,currWord)}))

    nextWord = currWord;
end


%[val,idx] = max(values(wdDic{lookup(mdP1Dic,currWord)}))


