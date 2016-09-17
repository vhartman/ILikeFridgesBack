import json
import pdb

error_margin = 0.5

def extract_rows(data):
	info_data = data["textAnnotations"]

	data_rows = []

	for entry in info_data:
		# skip the data about the whole receipt
		if "locale" in entry:
			continue

		vertices = entry["boundingPoly"]["vertices"]
		x_center = (vertices[0]["x"] + vertices[2]["x"])/2
		y_center = (vertices[0]["y"] + vertices[2]["y"])/2

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


def pretty_print(rows):
	object_count = 0

	for row_y, row in rows:
		row_str = "y: %d, " % row_y
		for column in row:
			row_str += (column["description"] + " ")
			object_count+=1
		print row_str

	return object_count



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
