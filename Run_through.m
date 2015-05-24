srcFiles = dir(pwd);  % the folder in which our images exists
for i = 1 : length(srcFiles)
    filename = strcat(srcFiles(i).name);
    if length(filename) >= 4
        if strcmp(filename(length(filename)-2:length(filename)),'jpg') == 1
            figure(1);
            I = imread(filename);
            imshow(filename);
            Manual(filename);
        end
    end
%     display(filename);
end

view_close = input('Want to close(yes/no)? ENTER: ', 's');
if view_close == 'yes'
    close all;
end
