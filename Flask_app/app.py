#from dotenv import load_dotenv
import os
import sys
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from api.utils import AZURE_STORAGE_CONNECTION_STRING,update_file,deleteFile,get_all_images,get_images_by_tags

# from Flask_app.api.utils import allowed_file, analysis_image, save_image_in_container, save_image_in_mysql

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
"""
@app.route('/getimages',methods= ['GET'])
def getImages():
    images = requests.get(base_api+'/getAll')
    return jsonify(images)

        #save_image_in_blob_and_tags_in_db
        resp = jsonify({'message' : 'File successfully uploaded and analysis', "data": tags_image_saved})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return res
"""        
    
@app.route('/getAll',  methods = ['GET'])
def get_all():
    d = get_all_images()
    print(d)
    return render_template("liste_images.html", images={'message' : 'All images', "data": d})

@app.route('/rechercher')
def render_search_page():
    return render_template("search.html")


@app.route('/search', methods = ['GET'])
def get_by_tags():
    if 'tags' in request.args:
        tags = request.args['tags']
        print(tags)
        res = get_images_by_tags(tags)
        resp = jsonify({'message' : 'File successfully uploaded and analysis', "name": ""})
        resp.status_code = 201
        return render_template("search.html")
    else:
        return "Image not Found"

   
 
@app.route('/deleteFile',  methods = ['POST','DELETE'])
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

@app.route('/updateFile',  methods = ['POST,PUT'])
def update_name():
    data = request.json
    update_file(data)
    resp = jsonify({'message' : 'File successfully updated', "data": data})
    resp.status_code = 201
    return resp       
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
