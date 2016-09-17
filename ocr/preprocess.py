import json

import sys

row_coeff = 2

def extract_rows(data):
	info_data = data["textAnnotations"]

	data_in_rows = {}

	for entry in info_data:
		vertices = entry["boundingPoly"]["vertices"]
		#x_center = (vertices[0]["x"] + vertices[3]["x"])/2
		y_center = (vertices[0]["y"] + vertices[3]["y"])/2
		
		#width 	= vertices[3]["x"] - vertices[0]["x"]
		height	= vertices[3]["y"] - vertices[0]["y"]

		for row_center in data_in_rows:
			if (row_center <= (y_center+height*row_coeff)) and (row_center >= (y_center - height*row_coeff)):
				# add object to the list for the row
				#print "to append"
				append_row_object(data_in_rows[row_center], entry)
				# change the current average horizontal center
				new_row_center = (row_center*(len(data_in_rows[row_center])-1) + y_center) / len(data_in_rows[row_center])

				row_list = data_in_rows[row_center]
				#data_in_rows.pop(row_center)
				#data_in_rows[new_row_center] = row_list

				data_in_rows[new_row_center] = data_in_rows[row_center]
				del data_in_rows[row_center]
				break

		# add a new row if not there
		else:
			data_in_rows[y_center] = []
			data_in_rows[y_center].append(entry)

		#print "added"

	return data_in_rows

def append_row_object(row_list, new_column):
	for idx, column in enumerate(row_list):
		if column["boundingPoly"]["vertices"][0]["x"] >= new_column["boundingPoly"]["vertices"][3]["x"]:
			row_list.insert(idx, new_column)
			return
	row_list.append(new_column)




def pretty_print(rows):
	for entry in rows:
		row = ""
		for column in rows[entry]:
			row += (column["description"] + " ")
		print row
			#sys.stdout.write(column["description"] + " ")

		#print "\n"

with open('data.json') as data_file:
	data = json.load(data_file)


rows = extract_rows(data)

#print "extracted"

pretty_print(rows)

