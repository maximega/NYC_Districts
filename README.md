How to Run Web App:

    1.) Run Flask app (python app.py) make sure to run on 8080

    2.) Open a chrome browser with security disabled (CORS issue):

    For PC: chrome.exe --user-data-dir="C://Chrome dev session" --disable-web-security

    For Mac: open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security

    3.) Open index.html inside that chrome browser (whole AngularJS front end is in this file; all js libraries are accessed with CDN's)  

    4.) If that doesn't work, either try quitting chrome, or using Firefox with a CORS plugin

  


  
