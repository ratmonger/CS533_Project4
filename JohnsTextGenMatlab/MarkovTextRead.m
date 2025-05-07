% fidMD = fopen('MobyDick.txt');
% MD=textscan(fidMD,'%s');     

MDtext = fileread('MDP1.txt');
MDtext = regexprep(MDtext, '[^\w\s]', ' ');
MDtext = regexprep(MDtext, '[\r]', ' ');
MDtext = regexprep(MDtext, '\s+', ' ');
% [~,mdsz] = size(MDtext);
% words = regexp(MDtext, '[\w+\s]', 'match');
% wordi = 1;
% letteri = 1;
% wordCounts = count(MDtext, ' ');
% wordArray = strings(wordCounts,1);
% nextWord = '';

% for i = 1:mdsz
%     if MDtext(i) ~=' '
%         nextWord(letteri) = MDtext(i);
%         letteri = letteri + 1;
%     else
%         letteri = 1;  
%         wordArray(wordi) = convertCharsToStrings(nextWord); 
%         nextWord = '';
%         wordi = wordi + 1;
%     end
% end



pat = lettersPattern;
words = extract(MDtext,pat);

wordCounts = count(words,pat);
histogram(wordCounts);