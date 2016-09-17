clc; close all; clear all;

%% Load + crop image

img_org = imread('../Data/20160916_234204.jpg'); % migros
%img_org = imread('../Data/20160916_234214.jpg'); % coop
img_resize = imresize(img_org, 0.2);
img_rot = imrotate(img_resize, 0);

figure(1)
imshow(img_rot);
% 
% figure(2)
% imshow(img_resize);

img_gray = rgb2gray(img_rot);
img_bw = im2bw(img_gray, 0.5);

figure(2)
imshow(img_bw);

s = regionprops(img_bw, 'Area', 'BoundingBox');
area = cat(1, s.Area);
bb = cat(1, s.BoundingBox);

[t, I] = sort(area, 'descend');

img_crop = imcrop(img_bw, bb(I(1), :));

figure(3)
imshow(img_crop);

%%

img_1D = sum(img_crop);

figure(5)
imshow(im2bw(img_1D/max(img_1D), 0.95));