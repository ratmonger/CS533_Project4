function arrayOfStructs = createFwProbabilities(fwfd,noa)
%createFwProbabilities Changes values of the fwfd dictionaries into
%probabilities
%   Detailed explanation goes here

    [~,sznoa] = size(noa);
    for i = 1:sznoa
       % fprintf("Original fwfd values for %d\n",i );
       % disp(entries(fwfd{i}));       
      
        currfwfdEntries = entries(fwfd{i});
        sumDic = sum(currfwfdEntries.Value);
        numEnt = numEntries(fwfd{i});
        dicKeys = keys(fwfd{i});
        runningTotal = 0;
        for j = 1:numEnt
            a = dicKeys(j);
            runningTotal = runningTotal+ lookup(fwfd{i},a)/sumDic;
            fwfd{i} = insert(fwfd{i},a,runningTotal);        
        end  
     % disp(entries(fwfd{i}));       
    end
    for j = 1:sznoa
        fwfdTable = (entries(fwfd{j}));
        % sortedfwfdTbl(:,j) = sortrows(fwfdTable, 'Value'); % sort the table by 'DOB'
       arrayOfStructs{j} = table2struct(sortrows(fwfdTable, 'Value')); % change it back to struct array if necessary
    end

end