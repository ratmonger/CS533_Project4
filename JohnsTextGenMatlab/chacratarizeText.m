% charactarizeText
% Creates a text dictionary (td) with an entery for each word
% creates a cell array of following word frequency dictionaries (fwfd) for the words following each word 
% the 
% inputs cell string array
% output td - one entry for each word non repeating
%        fwfd - a call array of dictionaries, one for for each entry in td
%               -each dictionary has an entry for each non repeating
%               instance of a following word matched with number of
%               occurences
%       total array - array of the number of occurences of each word in the
%       text


% Charactarize Tex (This name should change)


function [td,fwfd,totalArray] = chacratarizeText(textArrayIn)

    % create a dictionary
    td = createMainDictionary(textArrayIn);
    [fwfd, totalArray] = createWordDictionaries(td, textArrayIn);
% 


end

%%%%%%%%%%%% file functions%%%%%%%%%%%%%%%%%

% function to create a list of all words with no duplicates
% input is the string array of the text broken into words
% output is the dictionary one entry for each word
%       Keys are the word string
%       values is the index, points to the corosponding member of the fwfd 
function d = createMainDictionary(textArrayIn)
[numWrdsIntext,~] = size(textArrayIn);
% create a dictionary 
d = configureDictionary("string","double");
indx = 0;
    for i = 1:numWrdsIntext
        tf = isKey(d,textArrayIn(i)); 
        if tf == 0
            indx = indx +1;
            d = insert(d,textArrayIn(i),indx,"Overwrite",false);
        end
    end
end

%function to create a dictionary of follow words for ewach word in the text
% 
function [fwfd, totalArray] = createWordDictionaries(td, textArrayIn)
    [numWords,~] = size(textArrayIn);
    numEnt = td.numEntries;
    totalArray = zeros(1,numEnt);
    fwfd = {}; % is a cell array of dictionaries for each word where the dictionary are the words that follow 
    for i = 1:numEnt
        fwfd =[fwfd,num2cell(configureDictionary("string","double"))];
    end
    for i = 1:numWords-1 % do for each word
        currWord = textArrayIn(i); % get current word
        followingWord = textArrayIn(i+1); % get next word
        currWordIdx = lookup(td,currWord); % get the d index of the word
        currValue = lookup(fwfd{currWordIdx},followingWord,FallbackValue=0); 
        fwfd{currWordIdx} = insert(fwfd{currWordIdx},followingWord,currValue+1);
    end
 
    for i = 1:numEnt
        totalArray(i) = sum(values(fwfd{i}));
    end
end