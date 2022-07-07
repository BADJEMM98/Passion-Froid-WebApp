#from dotenv import load_dotenv
import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from api.utils import AZURE_STORAGE_CONNECTION_STRING, connect_to_azure, allowed_file,analysis_image,save_image_in_container

#load_dotenv('./.flaskenv')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.makedirs('uploads') if not os.path.exists('uploads') else os.path.abspath('uploads')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


MY_CONNECTION_STRING = "REPLACE_THIS"
MY_IMAGE_CONTAINER = "myimages"
#cors = CORS(app, resources={r"/": {"origins": "*"}})


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/uploadFile',  methods = ['POST'])
def uploadFile():
    print(request.files)
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    #file is correctly sent from resuaest and respect the format    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #analysis image
        image_analysis = analysis_image(filename)
        tags_image_saved= save_image_in_container(filename)
        #saved__in_mysql = save_tags_mysql()
        #save_image_in_blob_and_tags_in_db
        resp = jsonify({'message' : 'File successfully uploaded and analysis', "data": image_analysis})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
