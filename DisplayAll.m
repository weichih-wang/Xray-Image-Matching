srcFiles = dir(pwd);  % the folder in which our images exists
for i = 1 : length(srcFiles)
    filename = strcat(srcFiles(i).name);
    if length(filename) >= 4
        if filename(length(filename)-2:length(filename)) == 'jpg'
            figure(i);
            I = imread(filename);
            imshow(I);
        end
    end

%     display(filename);
end

view_close = input('Want to close(yes/no)? ENTER: ', 's');
if view_close == 'yes'
    close all;
end
