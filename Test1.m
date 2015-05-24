% function I = Test1(img)
% I = imread(img);

I = imread('0061_AP_1.11.10.jpg'); % Reads image onto I
K = imadjust(I,[0.50; 0.840],[]); % adjust intensity values of I
Igrey = rgb2gray(I); %convert to greyscale
imshow(K);
% figure(1); 
% imshow(I);
% figure(2);
% imshow(Igrey);

Iedge = edge(Igrey,'canny',[0, 0.2]); % runs canny edge detection --> Be able to detect edges of the entire skeleton
figure(3);
imshow(Iedge); 

% figure(4);
J = imadjust(I,stretchlim(I),[]);
% imshow(I), figure, imshow(J)
figure(4);
imshow(J);

%ICROP
% figure(5);
Icropedge = imcrop(Iedge, [900 3400 900 6000]);
Icrop = imcrop(Igrey, [900 3400 900 6000]);
% imshow(Icrop);

figure(6);
imshow(Icrop);


% imcontrast; %Window Minimum 120 Maximum 200 Width 80 Center 160
% Eliminate Outliers: 5% Min: 130 Max: 215 Width: 85 Center: 170