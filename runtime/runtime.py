import os,errno
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file,session, jsonify
from flask_bootstrap import Bootstrap
import sys
import json
import os
import socket

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
bootstrap = Bootstrap(app)

module_port_int = 3000
module_name_id_map = {}

def get_free_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port

def save_data():
    with open('module_name_id_map.json', 'w') as fp:
        json.dump(module_name_id_map, fp)

def load_data():
    with open('module_name_id_map.json', 'r') as fp:
        module_name_id_map = json.load(fp)
    print(module_name_id_map)


@app.route('/')
def landingPage():
    return "You are at Runtime module"

@app.route('/start/<module_name>', methods=['GET'])
def start_module(module_name):

    response = {}
    try:
        module_port = get_free_port()
        print("module_port: ",module_port)
        container_id = ""
        os.system("sudo docker run -p {}:{} -d {} > output.txt".format(module_port,module_port_int,module_name))

        if os.path.exists('output.txt'):
            fp = open('output.txt', "r")
            container_id = fp.read()
            fp.close()
            os.remove('output.txt')

        print("output: ",container_id)

        if container_id == "" or container_id is None:
            print("Deployment Failed")
            response["status"] = "failure"
            return jsonify(response)

        os.system("sudo docker ps -a")
        print('{} module deployed'.format(module_name))
        
        module_name_id_map[module_name] = container_id
        save_data()

        response["port"] = module_port
        response["status"] = "success"
        return jsonify(response)
    
    except Exception as e:
        print(e)
        response["status"] = "failure"
        return jsonify(response)

@app.route('/stop/<module_name>', methods=['GET'])
def stop_module(module_name):

    try:
        load_data()
        container_id = module_name_id_map[module_name]
        module_name_id_map.pop(module_name)
        save_data()
        os.system("sudo docker stop {}".format(container_id))
        os.system("sudo docker rm {}".format(container_id))

        if os.path.exists('output.txt'):
            fp = open('output.txt', "r")
            container_id = fp.read()
            fp.close()
            os.remove('output.txt')

        print("output: ",container_id)

        os.system("sudo docker ps -a")
        print('{} module stoped'.format(module_name))

        return "success"
    except Exception as e:
        print(e)
        return "failure"

if __name__=='__main__':
    app.run(host="127.0.0.1",debug=True,port=3000,threaded=True)
