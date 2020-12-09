
#ivri korem 2020
"""
HomeDrive is a REST API to store your private files in.
"""

#init
import os
from werkzeug.utils import secure_filename
from flask import (
	Flask,
	flash,
	request,
	redirect,
	url_for
)

#flask app
app = Flask(__name__)

#global vars
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}
UPLOAD_FOLDER = '/var/www/html/Storage'
USERS = os.listdir(UPLOAD_FOLDER) #needs to be permanent maybe a file
APACHE_URL = input("please enter the link to the apache server")

#routes & funcs
def checkFile(fileName):
	return	('.' in fileName) and (fileName.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

#handle USERS
def handleUsers(userName):
	if userName in USERS:
		print("user exists")
	else:
		print("Creating new user:"+userName)
		USERS.append(userName)
		os.mkdir(UPLOAD_FOLDER+"/"+userName.lower())

#handle post request
def uploadFile(request,userName):
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and checkFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER+'/'+userName.lower(), filename))
            #return redirect(url_for('transferFile', filename=filename))
        return "Finished Uploading!"

#handle get request
def downloadFile(request,userName):
	return """
	<!doctype html>
	<h1>Download User Files</h1>
	<a href="{}/Storage/{}" download>Download</a>
	""".format(APACHE_URL,userName.lower())

#api
@app.route('/api/<string:user>', methods=['GET','POST'])
def transferFile(user):
	#set or create target user
	handleUsers(user)

	#handle post request
	if request.method == 'POST':
		return uploadFile(request,user)

	#handle get request
	if request.method == 'GET':
		return downloadFile(request,user)

#ui
@app.route('/ui/<string:user>')
def handleUI(user):
	return  '''
    	<!doctype html>
    	<title>Upload new File</title>
    	<h1>Upload new File</h1>
    	<form method=post action="/api/{}" enctype="multipart/form-data">
        <input type=file name=file>
	<input type=submit value=Upload>
    	</form> '''.format(user)

#view
@app.route('/view/<string:user>', methods=['GET'])
def viewStorage(user):
	return str(os.listdir(UPLOAD_FOLDER+'/'+user.lower()))

#main
if __name__=="__main__":
	app.debug = True
	app.run(port=4444)
