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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Hack Zurich 2016 1022-9213bc019af2.json'
image = cv2.imread('Data/20160917_231054.jpg')

warped = transform_receipt_image(image)
if type(warped) != int:
    print "Warping"

    img_req = warped

    # cv2.imshow("Warped", warped)
    # cv2.waitKey(0)

    response = ocr.request(warped)
else:
    print "FFT2"
    img_s = transform.resize(image, height = 400)
    angle = compute_angle(img_s)

    img_req = transform.rotate(image, angle)

    # img_rot_disp = transform.rotate(img_s, angle)
    # cv2.imshow("Rotated", img_rot_disp)
    # cv2.waitKey(0)

img_req = transform.resize(img_req, height = 1000)
response = ocr.request(img_req)

cv2.imshow("Orginial", transform.resize(image, height = 800))
cv2.imshow("Request", img_req)
cv2.waitKey(0)

print response

rows = preprocess.extract_rows(response['responses'][0])
lower_block = preprocess.remove_lower(rows)
item_block = preprocess.remove_upper(lower_block)

preprocess.pretty_print(item_block)

# cv2.imshow("Warped", warped)
# cv2.imshow("Rotated", img_rot)
# cv2.waitKey(0)

# cv2.imshow("Scanned", transform.resize(warped, height = 650))
# cv2.waitKey(0)
