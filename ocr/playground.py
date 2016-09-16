import json
from pprint import pprint





if __name__ == '__main__':

    with open('data.json') as data_file:
        data = json.load(data_file)

    pprint(data)

