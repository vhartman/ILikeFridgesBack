import json
import numpy as np
import pdb

error_margin = 0.5

def extract_rows(data):
	info_data = data["textAnnotations"]

	data_rows = []

	for entry in info_data:
		# skip the data about the whole receipt
		if "locale" in entry:
			continue
		if entry["description"] == "l":
			entry["description"] = "1"
		vertices = entry["boundingPoly"]["vertices"]
		#x_center = (vertices[0]["x"] + vertices[2]["x"])/2
		#y_center = (vertices[0]["y"] + vertices[2]["y"])/2
		x_center, y_center = rectangle_center(entry)

		#width 	= vertices[2]["x"] - vertices[0]["x"]
		height	= (vertices[2]["y"] - vertices[0]["y"])

		for row_y, row in data_rows:
			if (row_y <= (y_center+height*error_margin)) and (row_y >= (y_center - height*error_margin)):

				# change the current average horizontal center
				row_y = (row_y*len(row) + y_center) / (len(row) + 1)

				# add object to the list for the row
				append_row_object(row, entry)
				#row.append(entry)
				break

		# add a new row if not there
		else:
			new_row = []
			new_row.append(entry)
			data_rows.append( (y_center,new_row) )

	return data_rows

def append_row_object(row, new_column):
	for idx, column in enumerate(row):
		if column["boundingPoly"]["vertices"][0]["x"] >= new_column["boundingPoly"]["vertices"][2]["x"]:
			row.insert(idx, new_column)
			return
	row.append(new_column)


def concatenate_strings(rows):
	concatenated_rows = []
	for row_y, row in rows:
		row[0]["description"] = fix_commas(row[0]["description"])
		concatenated_rows.append( (row_y, [row[0]]) )
		last_is_str = not is_number(row[0]["description"])
		for column in row[1:]:
			#if column["description"] == "3.84":
			#	pdb.set_trace()
			column["description"] = fix_commas(column["description"])
			y_coord, new_row = concatenated_rows[-1]
			if last_is_str and not is_number(column["description"]):			
				new_row[-1]["boundingPoly"]["vertices"][1] = column["boundingPoly"]["vertices"][1]
				new_row[-1]["boundingPoly"]["vertices"][2] = column["boundingPoly"]["vertices"][2]
				new_row[-1]["description"] += (" " + column["description"]) 
			else:
				new_row.append(column)

			if is_number(column["description"]):
				last_is_str = False
			else:
				last_is_str = True

	return concatenated_rows

def pretty_print_concatenated(rows):
	object_count = 0

	for row_y, row in rows:
		print "y: %d, " % row_y
		for column in row:
			print column["description"]
			object_count+=1
		print "------------------------- NEW ROW -------------------------"
	return object_count


def pretty_print(rows):
	object_count = 0

	for row_y, row in rows:
		row_str = "y: %d, " % row_y
		for column in row:
			row_str += (column["description"] + " ")
			object_count+=1
		print row_str

	return object_count


def remove_lower(resp):
    res = []
    y_lim = np.inf
    for row_y, row in resp:
        for column in row:
            if column['description'] == 'TOTAL' or column['description'] == 'TOTAL CHF' :
                y_lim = np.min([y_lim,row_y])

    for row_y, row in resp:
        if row_y < y_lim:
            res.append((row_y,row))

    return res

def remove_upper(block):
    block.reverse()
    item_block = []
    y_lim, row = block[0]
    row_distance = 1.5 * np.abs(row[1]['boundingPoly']['vertices'][3]['y']-
								row[1]['boundingPoly']['vertices'][0]['y'])

    for row_y, row in block:
        if np.abs(y_lim-row_y)>row_distance:
            y_lim = row_y
            break
        y_lim = row_y

    for row_y, row in block:
        if row_y > y_lim:
            item_block.append((row_y,row))

    item_block.reverse()

    return item_block

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        try:
        	float(s)
        	return True
        except ValueError:
	        return False

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
	    return False

def fix_commas(string):
	if "," not in string:
		return string
	return string.replace(",", ".")	        

def decimals(string):
	return len(string) - string.index('.') - 1


def make_amount_predictions(rows):
	for row_y, row in rows:
		for column in row:
			column["prediction"] = make_meaning_prediction(column['description'])


def make_meaning_prediction(string):
	prediction = "unknown"

	# String
	if not is_number(string): 
		if len(string) >= 3:
			prediction = "product"

	# Integer
	elif is_int(string): 
		if int(string) != 0:
			prediction = "amount"

	# Float - price
	elif decimals(string) == 2: 
		prediction = "price"

	# Float - amount
	elif decimals(string) == 3: 
		prediction = "amount"

	return prediction


def rectangle_center(json_obj):
	vertices = json_obj["boundingPoly"]["vertices"]
	x_center = (vertices[0]["x"] + vertices[2]["x"])/2
	y_center = (vertices[0]["y"] + vertices[2]["y"])/2
	return x_center, y_center


def amount_cluster_center(product_rows):
	amount_x = 0
	amount_count = 0
	product_x = 0
	product_count = 0
	price_x = 0
	price_count = 0
	for y_coord, product in product_rows:
		for column in product:
			if column["prediction"] == "amount":
				x_center, y_center = rectangle_center(column)
				amount_x += x_center
				amount_count+=1

	return amount_x/amount_count

# ====================================================== MAIN ======================================================


if __name__ == '__main__':
	with open('data.json') as data_file:
		data = json.load(data_file)


	rows = extract_rows(data)

	matched_objects = pretty_print(rows)

	print "\n\n"
	print "matched_objects = %d " % matched_objects
	print "original_objects = %d " % (len(data["textAnnotations"])-1)
	print "rows = %d"  % len(rows)



	lower_block = remove_lower(rows)
	item_block = remove_upper(lower_block)

	print "----------------------- PRODUCTS ONLY -----------------------"

	pretty_print(item_block)


	# CONCATENATE SINGLE STRINGS INTO PRODUCT NAMES

	concatenated_rows = concatenate_strings(item_block)
	concatenated_objects = pretty_print_concatenated(concatenated_rows)

	print "\n\n"
	print "concatenated_objects = %d " % concatenated_objects
	print "original_objects = %d " % (len(data["textAnnotations"])-1)
	print "rows = %d"  % len(rows)


	make_amount_predictions(concatenated_rows)
	amount_center = amount_cluster_center(concatenated_rows)


	print amount_center

	# MAKE PREDICTION ABOUT MEANING OF A FIELD



