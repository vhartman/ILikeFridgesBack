
import execjs
import os

def update_items(current_items, receipt_input):
	changed_items = []

	for product in receipt_input:
		changed_items.append(product)

		if product in current_items:
			current_items += receipt_input[product]
		else:
			current_items = receipt_input[product]

	return changed_items
"""
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

print ("PUT DONE")
st.child("images/20160916_234139.jpg").download("downloaded.jpg")
"""


os.environ["EXECJS_RUNTIME"] = "Node"

node = execjs.get("Node")

firebase_js = node.compile("""
function init_firebase(){
  var firebase = require("firebase");
  // Set the configuration for your app
  var config = {
    apiKey: 'AIzaSyAb8M6OlMBfGfg5XgJIkh5i4yO3KP2qu2o',
    authDomain: 'ilikefridges-735ac.firebaseapp.com',
    databaseURL: 'https://ilikefridges-735ac.firebaseio.com',
    storageBucket: 'ilikefridges-735ac.appspot.com'
  };
  firebase.initializeApp(config);

  return firebase;
}

function download_image(firebase){

  // Create a reference with an initial file path and name
  var storage = firebase.storage();
  //var pathReference = storage.ref('images/20160916_234139.jpg');
  var storageRef = storage.ref();

  // Create a reference from a Google Cloud Storage URI
  //var gsReference = storage.refFromURL('gs://bucket/images/20160916_234139.jpg')

  // Create a reference from an HTTPS URL
  // Note that in the URL, characters are URL escaped!
  //var httpsReference = storage.refFromURL('https://firebasestorage.googleapis.com/b/bucket/o/images%20stars.jpg');


  storageRef.child('images/20160916_234139.jpg').getDownloadURL().then(function(url) {
    // Get the download URL for 'images/stars.jpg'
    // This can be inserted into an <img> tag
    // This can also be downloaded directly
  }).catch(function(error) {
    // Handle any errors
  });

}
	""")


firebase = firebase_js.call("init_firebase")

firebase_js.call("download_iamge", firebase)


