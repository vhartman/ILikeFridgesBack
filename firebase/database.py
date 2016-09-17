
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

config = {
  "apiKey": "AIzaSyAb8M6OlMBfGfg5XgJIkh5i4yO3KP2qu2o",
  "authDomain": "ilikefridges-735ac.firebaseapp.com",
  "databaseURL": "https://ilikefridges-735ac.firebaseio.com",
  "storageBucket": "ilikefridges-735ac.appspot.com",
  "serviceAccount": "../Hack Zurich 2016 1022-9213bc019af2.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("devstar1022@gcplab.me", "yCYb9nedu9")

#print user

st = firebase.storage()

storage.child("images/example.jpg").put("example2.jpg", user['idToken'])

print "PUT DONE"
st.child("images/20160916_234139.jpg").download("downloaded.jpg")


"""
var config = {
    apiKey: "AIzaSyAb8M6OlMBfGfg5XgJIkh5i4yO3KP2qu2o",
    authDomain: "ilikefridges-735ac.firebaseapp.com",
    databaseURL: "https://ilikefridges-735ac.firebaseio.com",
    storageBucket: "ilikefridges-735ac.appspot.com",
    messagingSenderId: "843914572032"
  };
"""

