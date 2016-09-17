clc; close all; clear all;

%% Load + crop image

img_org = imread('../Data/20160916_234204.jpg'); % migros
img_org = imread('../Data/20160916_234214.jpg'); % coop

img_resize = imresize(img_org, 0.2);
img_rot = imrotate(img_resize, 0); % for test purposes

figure(1)
imshow(img_rot);

img_gray = rgb2gray(img_rot);
img_bw = im2bw(img_gray, 0.2);

figure(14)
imshow(img_bw);

s = regionprops(img_bw, 'Area', 'BoundingBox', 'Orientation');

% crop
area = cat(1, s.Area);
bb = cat(1, s.BoundingBox);

[~, I] = sort(area, 'descend');

img_crop = imcrop(img_rot, bb(I(1), :));

figure(3)
imshow(img_crop);

figure(13)
imshow(img_rot);
hold on
for i=1:length(bb)
    rectangle('Position', bb(i, :), 'EdgeColor','r', 'LineWidth',3);
end
hold off

% b&w
thresh = 0.1;
img_gray = rgb2gray(img_crop);
img_crop = im2bw(img_gray, thresh);

while sum(sum(img_crop))/(area(1)) > 0.925
    thresh = thresh + 0.01;
    img_crop = im2bw(img_gray, thresh);
end

figure(4)
imshow(img_crop)

%%

img_1D = sum(img_crop);

figure(5)
imshow(im2bw(img_1D/max(img_1D), 0.95));