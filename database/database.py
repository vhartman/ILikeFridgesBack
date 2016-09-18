
import pyrebase

def update_items(current_items, receipt_input):
	changed_items = []

	for product in receipt_input:
		changed_items.append(product)

		if product in current_items:
			current_items += receipt_input[product]
		else:
			current_items = receipt_input[product]

	return changed_items


def setup_pyrebase():

	config = {
	  "apiKey": "AIzaSyAb8M6OlMBfGfg5XgJIkh5i4yO3KP2qu2o",
	  "authDomain": "ilikefridges-735ac.firebaseapp.com",
	  "databaseURL": "https://ilikefridges-735ac.firebaseio.com",
	  "storageBucket": "ilikefridges-735ac.appspot.com",
	  "serviceAccount": "ILikeFridges-dd134404e804.json"
	}

	firebase = pyrebase.initialize_app(config)
	storage = firebase.storage()

	return storage

if __name__ == '__main__':

	storage = setup_pyrebase()

	storage.child("20160916_234139.jpg").download("downloaded.jpg")



