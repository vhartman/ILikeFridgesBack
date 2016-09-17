import os
import numpy as np
import cv2

from OcrApiRequest import ocr
from ocr import preprocess
from document_scanner.pyimagesearch import transform
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
from ocr.angle import compute_angle

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

image = cv2.imread('Data/20160916_234205.jpg')

angle = compute_angle(transform.resize(image, height = 500));
img_rot = transform.rotate(image, angle/3.1415*180)

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
