from OcrApiRequest import ocr
from document_scanner.pyimagesearch import transform
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
import cv2

image = cv2.imread('Data/20160916_234139.jpg')
warped = transform_receipt_image(image)
response = ocr.request(warped)



cv2.imshow("Scanned", transform.resize(warped, height = 650))
cv2.waitKey(0)