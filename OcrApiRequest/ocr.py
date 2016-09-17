import base64
import httplib2
import json

from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

def request(image):
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)

    image_content = base64.b64encode(image.read())
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        }]
    })
    response = service_request.execute()

    #label = response['responses'][0]['labelAnnotations'][0]['description']
    #print('Found label: %s for %s' % (label, photo_file))
    return response

if __name__ == '__main__':
    with open('../Data/20160916_234152.jpg', 'rb') as image:
        request(image)
    #request('../Data/20160916_234152.jpg')
