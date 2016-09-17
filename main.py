import os
import numpy as np
from OcrApiRequest import ocr
from ocr import preprocess
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
import cv2

from matplotlib import pyplot as plt

def remove_lower(resp):
    res = []
    for row_y, row in resp:
        for column in row:
            if column['description'] == 'TOTAL':
                y_lim = row_y
                break
    for row_y, row in resp:
        if row_y < y_lim:
            res.append(row)

    return res

# def remove_lower(resp):
#     res = []
#     for attr in response['responses'][0]['textAnnotations']:
#         #print attr
#         if attr['description'] == 'TOTAL':
#             y_lim = attr['boundingPoly']['vertices'][0]['y']
#             break
#     for attr in response['responses'][0]['textAnnotations']:
#         if attr['boundingPoly']['vertices'][0]['y'] < y_lim:
#             res.append(attr)
#
#     return res

image = cv2.imread('Data/20160917_091338.jpg')

img_d = transform.resize(image, height = 500)
img_gr = cv2.cvtColor(img_d, cv2.COLOR_BGR2GRAY)
(thresh, img_bw) = cv2.threshold(img_gr, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

fft = np.fft.fft2(img_bw);
ffts = np.fft.fftshift(fft)
mag = np.log(np.abs(ffts) + 1);

maximum = max(mag.max(axis = 1))
mag_n = mag/maximum

print maximum

w = len(mag_n)
h = len(mag_n[0])

max_hor_d = 0
angle = 0

mag_filt = mag

for i in range(w):
    for j in range(h):
        hor_d = h/2 - j
        ver_d = w/2 - i
        if mag_filt[i][j] <= 0.6*maximum:
            mag_filt[i][j] = 0
        elif abs(hor_d) > max_hor_d:
            max_hor_d = abs(hor_d)
            angle = np.arctan2(ver_d*h, hor_d*w)

img_rot = transform.rotate(-img_d, angle*180/3.1415)

cv2.imshow("Rotated", img_rot)
cv2.waitKey(0)

#mag_grey = cv2.cvtColor(mag, cv2.COLOR_BGR2GRAY)
#(_, mag_thresh) = cv2.threshold(mag_grey, 128, 255, cv2.THRESH_BINARY)

# plt.subplot(121),plt.imshow(img_bw, cmap = 'gray')
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(mag_crop)
# plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.show()

warped = transform_receipt_image(image)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Hack Zurich 2016 1022-9213bc019af2.json'
response = ocr.request(warped)

rows = preprocess.extract_rows(response['responses'][0])
lower_block = preprocess.remove_lower(rows)
item_block = preprocess.remove_upper(lower_block)

preprocess.pretty_print(item_block)

#block = get_item_block(lower_block)

#print block

#
# cv2.imshow("Scanned", transform.resize(warped, height = 650))
# cv2.waitKey(0)
