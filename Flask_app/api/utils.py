import uuid
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings, ContainerClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import json

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

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=storageassionfroid;AccountKey=hAm9mO7Cl1v9xhP+aTWqtWxgTSIEvFiJnT3P2FV+keUPrr/+aiDcwOk7mn7nJpEgvd8JyYp0h0Xg+AStbETovQ==;EndpointSuffix=core.windows.net"
AZURE_STORAGE_ACCOUNT_NAME = "storageassionfroid"
COG_KEY = '956e9fd75a8849c38215648054e55832'
COG_ENDPOPINT= 'https://res-comp-viz.cognitiveservices.azure.com/'
IMG_FOLDERS_LOCAL = os.path.abspath('uploads') + '/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
    to_save = {
      "tags": analysis.tags
    }

    #description = computervision_client.describe_image_in_stream(image_stream)
    return to_save


def save_image_in_blob():
  con = connect_to_azure()
  cont = create_container(con)
  pass


def save_tags_in_mysql():
  pass

