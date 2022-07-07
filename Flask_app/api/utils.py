import uuid
import os
import json

from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings, ContainerClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes

import mysql.connector
from mysql.connector import errorcode


AZURE_ACCOUNT_INFOS = {
    
    "cloudName": "AzureCloud",
    "homeTenantId": "c371d4f5-b34f-4b06-9e66-517fed904220",
    "id": "07132315-7964-40cc-a46f-b77a9f7d7424",
    "isDefault": True,
    "managedByTenants": [],
    "name": "Azure for Students",
    "state": "Enabled",
    "tenantId": "c371d4f5-b34f-4b06-9e66-517fed904220",
    "user": {
      "name": "gsegoun@myges.fr",
      "type": "user"
    }
  }

#AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=storageassionfroid;AccountKey=hAm9mO7Cl1v9xhP+aTWqtWxgTSIEvFiJnT3P2FV+keUPrr/+aiDcwOk7mn7nJpEgvd8JyYp0h0Xg+AStbETovQ==;EndpointSuffix=core.windows.net"
#AZURE_STORAGE_ACCOUNT_NAME = "storageassionfroid"

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=storageaccountazure94;AccountKey=NuqrL/XWJsaxgZ/b8BzngxQGGKhuOQvzCLDJSDgNl3T3l7/kXv7ZcKpEau9ZaoQlfWthh3QCIdMc+AStDdb8bw==;EndpointSuffix=core.windows.net"
AZURE_STORAGE_ACCOUNT_NAME = "storageaccountazure94"
COG_KEY = '956e9fd75a8849c38215648054e55832'
COG_ENDPOPINT= 'https://res-comp-viz.cognitiveservices.azure.com/'
IMG_FOLDERS_LOCAL = os.path.abspath('uploads') + '/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
SQL_SERVER = 'passion-mysql-server.mysql.database.azure.com'
SQL_DB = 'passiondb'
MYSQL_USERNAME = 'passionadmin'
MYSQL_PASSWORD = 'MonikMik17!'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def connect_to_azure():
    #connect to azure account
    connect_str = AZURE_STORAGE_CONNECTION_STRING
    return connect_str


def save_image_in_container(filename):
    con_str = connect_to_azure()
    print(con_str)
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(con_str)
    container_name = "passion-images" 
    container = blob_service_client.get_container_client(container_name)
    
    if not container.exists():
      container = blob_service_client.create_container(container_name)

    #container_client = blob_service_client.create_container(container_name)  # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    
    file_path = os.path.join(IMG_FOLDERS_LOCAL, filename)
    print("\nUploading to Azure Storage as blob:\n\t" + file_path)

    # Upload the created file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{filename}"

    print(url)
    return url


def analysis_image(img_name):
    print(f'Ready to use cognitive services at {COG_ENDPOPINT} using key {COG_KEY}')
    # Get a client for the computer vision service
    computervision_client = ComputerVisionClient(COG_ENDPOPINT, CognitiveServicesCredentials(COG_KEY))
    print(computervision_client)
    # Get the path to an image file
    image_path = IMG_FOLDERS_LOCAL + img_name

    # Specify the features we want to analyze
    features = ['Description', 'Tags', 'Adult', 'Objects', 'Faces']

    # Get an analysis from the computer vision service
    image_stream = open(image_path, "rb")
    analysis = computervision_client.describe_image_in_stream(image_stream, visual_features=features)
    print(analysis)
    tags = analysis.tags
    #description = computervision_client.describe_image_in_stream(image_stream)
    return tags

def connect_to_mysql():
  try:
    cnxn = mysql.connector.connect(user=MYSQL_USERNAME, password=MYSQL_PASSWORD, host=SQL_SERVER, port=3306, database=SQL_DB)
    print("Connection established")
   
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with the user name or password")
      return None
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
      return None
    else:
      print(err)
      return None
  else:
    return cnxn

def save_image_in_mysql(tags, url, name):
  cn  = connect_to_mysql()
  if cn:
    cursor = cn.cursor()
    #insert file
    img_query = "INSERT INTO images (name,bloblink) VALUES(%s,%s);"
    cursor.execute(img_query, (name,url))
    cursor.execute("SELECT LAST_INSERT_ID() from images")
    last_image_id = cursor.fetchall()[0][0]
    print("Finished inserting row into images.")
    cn.commit()
    cursor.close()
    cn.close()
    print(last_image_id)
    save_tags(tags)
    return last_image_id
    #insert tags


def save_tags(tags):
  print(tags)
  cn  = connect_to_mysql()
  if cn:
    cursor = cn.cursor()
    tag_list_tuples = [(x) for x in tags]
    tags_ids = []
    print(tag_list_tuples)
    tag_query = """ insert ignore into tags(name) values(%s)"""
    try:
      cursor.executemany(tag_query, tag_list_tuples)
      cn.commit()
    except:
      cn.rollback()
    tags_tuples = tuple(tags)
    cursor.execute("SELECT id from tags where name in"+ str(tags_tuples))
    tags_ids = cursor.fetchall()
    print(tags_ids)
    print("Finished inserting row into tags")


     def save_imagein_mysql(tags, url, name):
  cn  = connect_to_mysql()
  if cn:
    cursor = cn.cursor()
    #insert file
    img_query = "INSERT INTO images (name,bloblink) VALUES(%s,%s);"
    cursor.execute(img_query, (name,url))
    
    cursor.execute("SELECT LAST_INSERT_ID() from images")
    last_image_id = cursor.fetchall()[0][0]
    print("Finished inserting row into images.")
    return last_image_id

    #insert into asso table
    list_image_tag = []
    for r in tags_ids:
      list_image_tag.append((last_image_id,r[0]))
    image_tag_query = """ insert into tag_image(id_image, id_tag) values (%s, %s) """
    try:
      cursor.executemany(image_tag_query, list_image_tag)
      cnxn.commit()
    except:
      cnxn.rollback()
    print("Finished inserting row into tag_image")

    # Cleanup
    cnxn.commit()
    cursor.close()
    cnxn.close()
    print("Done.")

"""def get_images():
  cursor.execute("SELECT * FROM images;")
  rows = cursor.fetchall()
  for row in rows:
    print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

"""



 