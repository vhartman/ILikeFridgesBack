import json
import numpy as np

import sys

row_coeff = 2


def get_item_block(data):

    max_y = np.inf
    for entry in data:
        if entry["description"] == "Total" or entry["description"] == "total":
            max_y = entry["boundingPoly"]["vertices"][0]["y"]
            break

    limit = len(data)
    i = 0
    while i < limit:
        if data[i]["boundingPoly"]["vertices"][0]["y"] > max_y:
            print 'I now delete '
            del data[i]
            limit -= 1

        i += 1

    return data
