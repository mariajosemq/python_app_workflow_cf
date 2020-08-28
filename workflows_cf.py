import json
from flask import Flask, request, jsonify 
from flask_cors import CORS, cross_origin
import requests
import objectpath
import os

app = Flask(__name__) 
port = int(os.getenv("PORT", 9009)) # port for local testing

@app.route('/TechnicalAuthentication', methods=['POST']) 
def conversationalAi():
  postRece = json.loads(request.get_data()) # getting data from the Conversational AI Bot memory
  phone = postRece['conversation']['memory']['phone']['raw'] # getting phone entity from the Bot memory
  status = triggerWorkflow(phone) # calling the Workflow Instance Trigger function, passing the phone as argument
  data = None

  if len(phone) > 0:
      if status == 201:
            data = jsonify( 
                  status=200, 
                  replies=[{'type': 'text','content': 'El Flujo de Trabajo se ha iniciado.'}] ) # sending message back to the Conversational AI Bot as a text message
      else: 
            data = jsonify( 
                  status=200, 
                  replies=[{'type': 'text','content': 'Ha surgido un error al accionar el flujo de trabajo. Por favor intentar en otra ocasión.'}] ) # sending message back to the Conversational AI Bot as a text message     
  return data

def triggerWorkflow(phone): #placing phone as parameter of the function
  
  s = requests.session() # Creating the session

  URL = "<url>/oauth/token?grant_type=client_credentials" # url gotten from the Workflow Service Instance Key
  
  HEADERS = {'Authorization': "Basic <cliendid and clientsecret credentials in base64>"}  # Basic Authorization in base 64, clientid is user and cliendsecret is the password

  r = s.get(url=URL,headers=HEADERS)  # sending get request and saving the response as response object

  access_token = r.json()['access_token']  # getting the access token
  token = "Bearer {}".format(access_token) # formatting the access token as needed in the header to post
  
  URL = "<workflow_rest_url>/v1/workflow-instances" #  url gotten from the Workflow Service Instance Key

  HEADERS = {'Authorization': token, "Content-Type":"application/json"}

  JSON = {
  "definitionId": "<your workflow definitionId>",
  "context": {
    "product": "Camera",
    "phone": phone,
    "price": 100
    }
  }
  r = s.post(url=URL,headers=HEADERS, json=JSON) # posting the payload with the specified headers and url

  return r.status_code # returning the status code of the function

@app.route('/errors', methods=['POST']) 
def errors(): 
  json.loads(request.get_data())
  return jsonify(status=200) 
 
app.run(host='0.0.0.0',  port=port) #importante indicar host para deployment en plataforma