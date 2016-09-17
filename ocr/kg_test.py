"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib

api_key = 'AIzaSyBoMOoG5UcWVBskmZLfKIOqR1lQC3dFHUs'
query = 'Strawberry'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': 10,
    'indent': True,
    'key': api_key,
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
for element in response['itemListElement']:
  print element['result']['name'] + ' (' + str(element['resultScore']) + ')'