import os
from OcrApiRequest import ocr
from ocr.get_item_block import get_item_block
from ocr.preprocess import extract_rows
from document_scanner.pyimagesearch import transform
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
import cv2

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

image = cv2.imread('Data/20160916_234139.jpg')
warped = transform_receipt_image(image)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Hack Zurich 2016 1022-9213bc019af2.json'
response = ocr.request(warped)

response = extract_rows(response['responses'][0])
#print response

lower_block = remove_lower(response)
print lower_block


#block = get_item_block(lower_block)

#print block


cv2.imshow("Scanned", transform.resize(warped, height = 650))
cv2.waitKey(0)
