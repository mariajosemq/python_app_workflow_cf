import asyncio
import websockets
import json
from flask import Flask, request, jsonify 
from flask_cors import CORS, cross_origin
import requests
import objectpath
import os
from random import randint

app = Flask(__name__) 
port = int(os.getenv("PORT", 9009)) # definicion de puerto de salida

@app.route('/test', methods=['POST']) 
def chatbot():
  #postRece = json.loads(request.get_data())
  #caso = postRece['conversation']['memory']['caso']['raw']
  caso = "reserva"
  status = triggerWorkflow(caso)
  data = None

  if caso == "compra":
      if status == 201:
            data = jsonify( 
                  status=200, 
                  replies=[{'type': 'text','content': 'El Flujo de Trabajo para solicitar la aprobación de la compra se ha iniciado.'}] )
      else: 
            data = jsonify( 
                  status=200, 
                  replies=[{'type': 'text','content': 'Ha surgido un error al accionar el flujo de trabajo. Por favor intentar en otra ocasión.'}] )        
  else:
      if status == 201:
            data = jsonify( 
                  status=200, 
                  replies=[{'type': 'text','content': 'El Flujo de Trabajo para solicitar la aprobación de la reserva se ha iniciado.'}] )
      else: 
            data = jsonify( 
                 status=200, 
                 replies=[{'type': 'text','content': 'Ha surgido un error al accionar el flujo de trabajo. Por favor intentar en otra ocasión.'}] ) 

  return data

def triggerWorkflow(caso):
  
  s = requests.session() #Creating session

  URL = "https://XXXXXXtrial.authentication.us10.hana.ondemand.com/oauth/token?grant_type=client_credentials"
	
  # Basic Authorization in base 64, clientid is user and cliendsecret is the password
  HEADERS = {'Authorization': "Basic XXXXXX"}
	 
  # sending get request and saving the response as response object
  r = s.get(url=URL,headers=HEADERS)
  
  access_token = r.json()['access_token'] # Obteniendo token, 
  token = "Bearer {}".format(access_token)
  print(token)
  
  URL = "https://api.workflow-sap.cfapps.us10.hana.ondemand.com/workflow-service/rest/v1/workflow-instances"
   # defining a params dict for the parameters to be sent to the API
  HEADERS = {'Authorization': token, "Content-Type":"application/json"}

  JSON = {
  "definitionId": "approvalworkflow",
  "context": {
    "product": "majo test",
    "price": 3.0,
    "caso": caso
    }
}
  r = s.post(url=URL,headers=HEADERS, json=JSON)
  print(r.status_code)

  # extracting data in json format "jsonify(r.json())", header (muestra el status 200 o cualquier otro) y body (payload). si es el estatus nada mas sería r.status_code
  return r.status_code
  #############################

@app.route('/errors', methods=['POST']) 
def errors(): 
  json.loads(request.get_data())
  return jsonify(status=200) 
 
app.run(host='0.0.0.0',  port=port) #importante indicar host para deployment en plataforma