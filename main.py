import os
from OcrApiRequest import ocr
from ocr.get_item_block import get_item_block
from ocr import preprocess
from document_scanner.pyimagesearch import transform
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
import cv2
import numpy as np

def remove_lower(resp):
    res = []
    y_lim = np.inf
    for row_y, row in resp:
        for column in row:
            if column['description'] == 'TOTAL' or column['description'] == 'TOTAL CHF' :
                y_lim = np.min([y_lim,row_y])

    for row_y, row in resp:
        if row_y < y_lim:
            res.append((row_y,row))

    return res

def remove_upper(block,row_distance):
    block.reverse()
    item_block = []
    y_lim, _ = block[0]
    for row_y, row in block:
        if np.abs(y_lim-row_y)>row_distance:
            y_lim = row_y
            break
        y_lim = row_y

    for row_y, row in block:
        if row_y > y_lim:
            item_block.append((row_y,row))

    item_block.reverse()

    return item_block

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
warped = transform_receipt_image(image)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Hack Zurich 2016 1022-9213bc019af2.json'
response = ocr.request(warped)

response = preprocess.extract_rows(response['responses'][0])

lower_block = remove_lower(response)
item_block = remove_upper(lower_block,80)
preprocess.pretty_print(item_block)


#block = get_item_block(lower_block)

#print block

#
# cv2.imshow("Scanned", transform.resize(warped, height = 650))
# cv2.waitKey(0)
