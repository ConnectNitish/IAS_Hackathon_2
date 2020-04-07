import os,errno
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file,session
from flask_bootstrap import Bootstrap
import requests
import sys

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
bootstrap = Bootstrap(app)

runtime_ip = "0.0.0.0"
runtime_port = 3000

@app.route('/')
def landingPage():
    return "You are at Deployer module"

@app.route('/start/<ip>/<port>/<module_name>', methods=['GET'])
def start_service(ip,port,module_name):
    
    try:
        print(module_name,ip,port)
        return requests.get('http://{}:{}/start/{}/{}'.format(runtime_ip,runtime_port,module_name,port)).content.decode("utf-8")
    except:
        return "failure"


@app.route('/stop/<ip>/<port>/<module_name>', methods=['GET'])
def stop_service(ip,port,module_name):

    try:
        print(module_name,ip,port)
        return requests.get('http://{}:{}/stop/{}'.format(runtime_ip,runtime_port,module_name)).content.decode("utf-8")
    except:
        return "failure"

if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True,port=5000,threaded=True)
