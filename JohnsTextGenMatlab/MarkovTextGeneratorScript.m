% [outputTextFile, fwfd,noa] = MarkovTextGenerator(inputFileName,outputFileName)
% MarkovTextGenerator Creates a text file based on the following word
% frequency of an existing text
%   Detailed explanation goes here
% input: tHE NAME OF AN EXISTING FILE
[InputFileText,InputFileWrdCnt] = TextFileExtract(inputFileName);% Read
[td,fwfd,noa] = chacratarizeText(InputFileText)%Create Dictionaries
sortedFwfdStruct = createFwProbabilities(fwfd,noa);
outputTextFile = {"This is the default Text"};
outputTextFile = createNewTextFile(td,sortedFwfdStruct,'one',10)
cellArray = cellstr(outputTextFile);
writecell(cellArray,outputFileName);




