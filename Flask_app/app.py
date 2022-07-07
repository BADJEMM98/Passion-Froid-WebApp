#from dotenv import load_dotenv
import os
import sys
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
# from api.utils import AZURE_STORAGE_CONNECTION_STRING, connect_to_azure, allowed_file,analysis_image,save_image_in_container,save_image_in_mysql
import mysql.connector
from mysql.connector import errorcode

# server = 'your_server.database.windows.net'
SQL_SERVER = 'passion-mysql-server.mysql.database.azure.com'
SQL_DB = 'passiondb'
USERNAME = 'passionadmin'
PASSWORD = 'MonikMik17!'
#load_dotenv('./.flaskenv')

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = os.makedirs('uploads') if not os.path.exists('uploads') else os.path.abspath('uploads')
# app.config['DOWNLOAD_FOLDER'] = os.makedirs('downloads') if not os.path.exists('downloads') else os.path.abspath('downloads')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#cors = CORS(app, resources={r"/": {"origins": "*"}})


@app.route('/')
def hello():
    return render_template("base.html")
@app.route('/getimages')
def getImages():
    try:
        cnxn = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=SQL_SERVER, port=3306, database=SQL_DB)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM images")
        rows = cursor.fetchall()

    
    return json.dumps(rows)

# @app.route('/uploadFile',  methods = ['POST'])
# def uploadFile():
#     print(request.files)
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         resp = jsonify({'message' : 'No file part in the request'})
#         resp.status_code = 400
#         return resp
#     file = request.files['file']
#     if file.filename == '':
#         resp = jsonify({'message' : 'No file selected for uploading'})
#         resp.status_code = 400
#         return resp
#     #file is correctly sent from resuaest and respect the format    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         print(filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #analysis image
#         tags_image_saved= analysis_image(filename)
#         url_image_saved = save_image_in_container(filename)
#         print(save_image_in_mysql(tags_image_saved, url_image_saved,filename))

#         #save_image_in_blob_and_tags_in_db
#         resp = jsonify({'message' : 'File successfully uploaded and analysis', "data": tags_image_saved})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
#         resp.status_code = 400
#         return resp

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
