function words = TextRead(fileName)    
    MDtext = fileread(fileName);
    MDtext = regexprep(MDtext, '[^\w\s]', ' ');
    MDtext = regexprep(MDtext, '[\r]', ' ');
    MDtext = regexprep(MDtext, '\s+', ' ');
    pat = lettersPattern;
    words = extract(MDtext,pat);
    wordCounts = count(words,pat);
end