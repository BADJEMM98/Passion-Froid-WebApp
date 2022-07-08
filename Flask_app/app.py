#from dotenv import load_dotenv
import os
import sys
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from api.utils import AZURE_STORAGE_CONNECTION_STRING,update_file,deleteFile,get_all_images,get_images_by_tags,allowed_file, analysis_image, save_image_in_container, save_image_in_mysql


SQL_SERVER = 'passion-mysql-server.mysql.database.azure.com'
SQL_DB = 'passiondb'
USERNAME = 'passionadmin'
PASSWORD = 'MonikMik17!'

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/')
def hello():
    return render_template("base.html")

@app.route('/getAll',  methods = ['GET'])
def get_all():
    d = get_all_images()
    print(d)
    return render_template("liste_images.html", images={'message' : 'All images', "data": d})

@app.route('/rechercher')
def render_search_page():
    return render_template("search.html")

@app.route('/uploadimages')
def render_upload_page():
    return render_template("upload.html")

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
        tags_image_saved= analysis_image(filename)
        url_image_saved = save_image_in_container(filename)
        print(save_image_in_mysql(tags_image_saved, url_image_saved,filename))

        #save_image_in_blob_and_tags_in_db
        resp = jsonify({'message' : 'File successfully uploaded and analysis', "data": tags_image_saved})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route('/search', methods = ['GET'])
def get_by_tags():
    if 'tags' in request.args:
        tags = request.args['tags']
        print(tags)
        res = get_images_by_tags(tags)
        resp = jsonify({'message' : 'File successfully uploaded and analysis', "name": ""})
        resp.status_code = 201
        return render_template("search_result.html", images=res)
    else:
        return "Image not Found"

 
@app.route('/deleteFile',  methods = ['DELETE'])
def delete_File():
    request.args.get("id")
    if 'id' in request.args:
        id = request.args['id']
        deleteFile(id)
        resp = jsonify({'message' : 'File successfully deleted', "id": id})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'No file selected for deleting'})
        resp.status_code = 400
        return resp

@app.route('/updateFile',  methods = ['PUT'])
def update_name():
    data = request.get_json()
    update_file(data)
    resp = jsonify({'message' : 'File successfully updated', "data": data})
    resp.status_code = 201
    return resp       


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
