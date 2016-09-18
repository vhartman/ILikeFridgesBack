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