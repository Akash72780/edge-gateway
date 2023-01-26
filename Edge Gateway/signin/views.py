from fileinput import filename
from tempfile import template
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from time import time
from pathlib import Path
import os, uuid
import json

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

values={}
error={}
def index(request):
    error["msg"]="Please login with correct info"
    template = loader.get_template('index.html')
    return HttpResponse(template.render(error, request))

def home(request):
    p_user = request.POST.get('userid')
    p_password = request.POST.get('password')
    if (p_user == "Service") and (p_password == "123456"):
        values["user"]=p_user
        values["password"]=p_password
        template = loader.get_template('home.html')
        return HttpResponse(template.render(values, request))
    else:
        template = loader.get_template('index.html')
        error["msg"]="User name or password is incorrect"
        return HttpResponse(template.render(error, request))
    
    


def add(request):
    p_server = request.POST.get('p_server')
    p_port = request.POST.get('p_port')
    # values = {
    #     "server": p_server,
    #     "port": p_port,
    # }
    # code should be added here
    try:
        connectionString = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container_name = "mblob"
        
        values["server"]=p_server
        values["port"]=p_port
        
        #create file
        fileName="info"+str(int(time() * 1000))+".json"
        
        with open("info/"+fileName,"w") as outfile:
            json.dump(values, outfile)
            
        # Get full path to the file
        upload_file_path = os.path.join(BASE_DIR, "info/"+fileName)

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connectionString)
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=fileName)

        print("\nUploading to Azure Storage as blob:\n\t" + fileName)
        
        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
            
        if os.path.exists("info/"+fileName):
            os.remove("info/"+fileName)

        # Upload the created file
        # with open(upload_file_path, "rb") as data:
        #     blob_client.upload_blob(data)
    except Exception as ex:
        print('Exception:')
        print(ex)
    # end of code
    template = loader.get_template("field_add.html")
    return HttpResponse(template.render(values, request))
