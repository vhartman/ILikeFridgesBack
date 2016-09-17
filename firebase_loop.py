from firebase import firebase
import os

from OcrApiRequest import ocr
from ocr import preprocess
from document_scanner.pyimagesearch import transform
from document_scanner.pyimagesearch.transform_receipt_image import transform_receipt_image
from ocr.angle import compute_angle


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Hack Zurich 2016 1022-9213bc019af2.json'
firebase = firebase.FirebaseApplication('https://ilikefridges-735ac.firebaseio.com', None)

while True:

    # check for flag
    while True:
        flag = firebase.get('flag/0',None)
        if flag['state'] == 'True':
            result = firebase.put('flag', '0', {'state': 'False'})
            items = firebase.get('items',None)
            break

    # download


    # image processing
    response = []

    # text processing
    rows = preprocess.extract_rows(response['responses'][0])
    lower_block = preprocess.remove_lower(rows)
    item_block = preprocess.remove_upper(lower_block)

    # get changes


    # iterate through list
    changes = []
    for id,object in changes:
        result = firebase.put('items', id, object)

# result = firebase.put('items', '3', {'description': 'mehh','amount':'100'})
# json_object = {'description': 'mehh','amount':'100','id':'3'}
# return_code = subprocess.call(["curl" "-X" "PUT" "-d" "' " + json_object + " https://samplechat.firebaseio-demo.com/'")
# post('itemss/1', {'description': 'mehh','amount':'100','id':'3'})
# print result
#
# curl -X PUT -d '{ "first": "Jack", "last": "Sparrow" }' \
#   'https://samplechat.firebaseio-demo.com/users/jack/name.json'