%probability Sctript
[Text1txt,txtWrdCnt] = TextFileExtract('Text1.txt');
[td,fwfd,noa] = chacratarizeText(Text1txt);

numWdEnt = numEntries(fwfd);
for i = 1:numWdEnt-1
    oneDic(i) = fwfd{i};
end

onesEnt = entries(oneDic);
onesEnt.Variables
onesEnt.Value
sumDic = sum(onesEnt.Value);
numEnt = numEntries(oneDic);
dicKeys = keys(oneDic);
for i = 1:numEnt
    a = dicKeys(i); 
    oneDic = insert(oneDic,a,lookup(oneDic,a)/sumDic);

end
oneDic;

dicStruct = table2struct(entries(oneDic));

%pic structure element
% choose based on probability
%sort
T = struct2table(dicStruct); % convert the struct array to a table
sortedT = sortrows(T, 'Value'); % sort the table by 'DOB'
sorteddicStruct = table2struct(sortedT); % change it back to struct array if necessary


for i = 2:numEnt
    sorteddicStruct(i).Value = sorteddicStruct(i).Value+sorteddicStruct(i-1).Value;
end
rnd = rand();
for i = 1:numEnt
   if sorteddicStruct(i).Value > rnd
       break;
   end
end
chosenval = sorteddicStruct(i).Key;

disp(chosenval)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%oneDic("two")
%oneDic("five")

      % for i = 2:numEnt
      %       sortedFwfdStruct(i).Value = sortedFwfdStruct(i).Value+sortedFwfdStruct(i-1).Value;
      %   end
      %   rnd = rand();
      %   for i = 1:numEnt
      %      if sortedFwfdStruct(i).Value > rnd
      %          break;
      %      end
      %   end
      %   chosenval = sortedFwfdStruct(i).Key;
      % 
      %   disp(chosenval)