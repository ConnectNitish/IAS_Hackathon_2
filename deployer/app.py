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

if __name__=='__main__':
    app.run(host="127.0.0.1",debug=True,port=5000,threaded=True)
