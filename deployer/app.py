import os,errno
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file,session, jsonify
from flask_bootstrap import Bootstrap
import requests
import sys
import json

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
bootstrap = Bootstrap(app)

load_balancer_ip = "127.0.0.1"
load_balancer_port = "7000"

@app.route('/')
def landingPage():
    return "You are at Deployer module"

@app.route('/start/<ip>/<port>/<module_name>', methods=['GET'])
def start_service(ip,port,module_name):

    print("Inside start_service deployment 99999999999999999999999999")

    try:
        print(module_name,ip,port)
        reponse = requests.get('http://{}:{}/start/{}'.format(ip,port,module_name)).content
        reponse = json.loads(reponse.decode('utf-8'))

        # if reponse["status"] == "success":
        #     reponse["status"] = requests.get('http://{}:{}/register/{}/{}/{}'.
        #         format(load_balancer_ip,load_balancer_port,module_name,ip,response["port"])).content.decode("utf-8")

        return reponse["status"]
    except Exception as e:
        print(e)
        return "failure"


@app.route('/stop/<ip>/<port>/<module_name>', methods=['GET'])
def stop_service(ip,port,module_name):

    try:
        print(module_name,ip,port)
        return requests.get('http://{}:{}/stop/{}'.format(ip,port,module_name)).content.decode("utf-8")
    except Exception as e:
        print(e)
        return "failure"


global kafka_IP_plus_port
global Deployment_Service_ip_port

kafka_IP_plus_port = None
Deployment_Service_ip_port = None
import requests 

repository_URL = "http://"+sys.argv[1]

def get_ip_port(module_name):
    custom_URL = repository_URL+"/get_running_ip/"+module_name
    r=requests.get(url=custom_URL).content
    r = r.decode('utf-8')
    print(r)
    return r

def get_Server_Configuration():
    global kafka_IP_plus_port 
    kafka_IP_plus_port = get_ip_port("Kafka_Service")

    if __debug__:
        print(" Kafka IP and Port",kafka_IP_plus_port)
    
    global Deployment_Service_ip_port
    Deployment_Service_ip_port = get_ip_port("Deployment_Service")
    
    if __debug__:
        print(" Deployment_Service_ip_port ",Deployment_Service_ip_port)

def get_ip_and_port(socket):
    ip_port_temp = socket.split(':')
    print(ip_port_temp)
    return ip_port_temp[0],ip_port_temp[1]

if __name__ == '__main__':

    print (' Initiating Deployer ')
    get_Server_Configuration()
    Deployment_Service_ip,Deployment_Service_port = get_ip_and_port(Deployment_Service_ip_port)

    if __debug__:
        print("Deployment_Service_ip,Deployment_Service_port",Deployment_Service_ip,Deployment_Service_port)

    app.run(host=Deployment_Service_ip,debug=False,port=int(Deployment_Service_port),threaded=True)
