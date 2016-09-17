import json
from pprint import pprint

if __name__ == '__main__':

    with open('data.json') as data_file:
        data = json.load(data_file)

    test = {"Name": 1, "Test": 2}

    for value in data["textAnnotations"]:
        # description field is the identified word
        pprint(value["description"])
        # boundingPoly/vertices gives the coordinates
        pprint(value["boundingPoly"]["vertices"])
