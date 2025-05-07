function writeNewTextFile(outputTextFile,outputFileName)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
    fid01=fopen(outputFileName,'w' );
    for i=1:length(outputTextFile)
        fprintf(fid01,'%s ',outputTextFile(i));
        if 0 == mod(i,12)
            fprintf(fid01,'\n');
        end
    end
    fclose('all');
end