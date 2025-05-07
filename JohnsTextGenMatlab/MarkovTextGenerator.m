function [outputTextFile, fwfd,noa] = MarkovTextGenerator(inputFileName,outputFileName,seedWord)
% MarkovTextGenerator Creates a text file based on the following word
% frequency of an existing text
%   Detailed explanation goes here
% input: tHE NAME OF AN EXISTING FILE
[InputFileText,InputFileWrdCnt] = TextFileExtract(inputFileName);% Read
[td,fwfd,noa] = chacratarizeText(InputFileText);%Create Dictionaries
sortedFwfdStruct = createFwProbabilities(fwfd,noa);
outputTextFile = createNewTextFile(td,sortedFwfdStruct,seedWord,InputFileWrdCnt);
% cellArray = cellstr(outputTextFile);
% writecell(cellArray,outputFileName);
writeNewTextFile(outputTextFile,outputFileName);
end




