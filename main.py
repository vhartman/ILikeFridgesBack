import os
from OcrApiRequest import ocr
from ocr import preprocess
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
import cv2


image = cv2.imread('Data/20160916_234205.jpg')
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
