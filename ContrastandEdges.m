% function I = Test1(img)
% I = imread(img);
I = imread('0061_AP_1.11.10.jpg');
K = imadjust(I,[0.53; 0.95],[]);
figure(3);
Igrey = rgb2gray(K);
imshow(Igrey);
% figure(1);
% imshow(I);
% figure(2);
% imshow(Igrey);
Iedge_c = edge(Igrey,'canny',[0 .2]);
Iedge_p = edge(Igrey,'prewitt');
% figure(3);
imshow(Iedge_c);

% figure(4);
J = imadjust(I,stretchlim(I),[]);
% imshow(I), figure, imshow(J)


%ICROP
% figure(5);
Icropedge = imcrop(Iedge_c, [900 3400 900 6000]);
Icrop = imcrop(Igrey, [900 3400 900 6000]);
% imshow(Icrop);

figure(1);
imshow(Icropedge);

figure(2);
s  = regionprops(Icropedge, 'centroid');
centroids = cat(1, s.Centroid);
imshow(Icropedge);
hold on;
plot(centroids(:,1), centroids(:,2), 'b*');
hold off;

% imcontrast; %Window Minimum 120 Maximum 200 Width 80 Center 160
%Eliminate Outliers: 5% Min: 130 Max: 215 Width: 85 Center: 170
