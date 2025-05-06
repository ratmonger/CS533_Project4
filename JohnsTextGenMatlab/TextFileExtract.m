% TextFileExtract
% Reads File, Remoes punctuation, carrage returns and excess whitespaces
% Input: the file name
% Output Cell array of strings
%        Number of cells

function [words, wdCnt] = TextFileExtract(fileName)    
    filetext = fileread(fileName);
    filetext = regexprep(filetext, '[^\w\s]', ' '); % remove non ltr/num/ws
    filetext = regexprep(filetext, '[\r]', ' ');    % remove carraigereturns
    filetext = regexprep(filetext, '\s+', ' ');     % remove multiple whitepaces
    pat = lettersPattern;
    words = extract(filetext,pat);          % extract words into cell array
    wordCount = count(words,pat);   
    wdCnt=sum(wordCount);                   % count all words
end