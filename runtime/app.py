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

module_port_int = 8100
module_name_id_map = {}
module_name_id_map_filepath = os.getcwd()+"/module_name_id_map.json"

def get_free_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port

def save_data():
    with open(module_name_id_map_filepath, 'w') as fp:
        json.dump(module_name_id_map, fp, indent=4, sort_keys=True)

def load_data():
    with open(module_name_id_map_filepath, 'r') as fp:
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

        response["service_port"] = str(module_port)
        response["machine_port"] = "3000"
        response["service_ip"] = "0.0.0.0"
        response["machine_ip"] = "127.0.0.1"

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
        
        module_name_id_map[container_id[:20]] = {
        "container_id":container_id,
        "module_name":module_name
        }
        save_data()

        response["uid"] = container_id[:20]
        response["status"] = "success"
        return jsonify(response)
    
    except Exception as e:
        print(e)
        response["status"] = "failure"
        return jsonify(response)

@app.route('/stop/<module_name>', methods=['GET'])
def stop_module(module_id):

    try:
        load_data()
        container_id = module_name_id_map[module_id]["container_id"]
        module_name_id_map.pop(module_id)
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
        print('{} module with id {} stoped'.format(module_name,module_id))

        return "success"
    except Exception as e:
        print(e)
        return "failure"

global kafka_IP_plus_port
global runtime_application_ip_port

kafka_IP_plus_port = None
runtime_application_ip_port = None

app.deployment_file_location = 'deployment/to_deploy_folder'
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
    
    global runtime_application_ip_port
    runtime_application_ip_port = get_ip_port("Runtime_Application")
    
    if __debug__:
        print(" runtime_application_ip_port ",runtime_application_ip_port)

def get_ip_and_port(socket):
    ip_port_temp = socket.split(':')
    print(ip_port_temp)
    return ip_port_temp[0],ip_port_temp[1]

if __name__=='__main__':
    
    get_Server_Configuration()
    runtime_application_ip,runtime_application_port = get_ip_and_port(runtime_application_ip_port)

    if __debug__:
        print(" runtime_application_ip,runtime_application_port ",runtime_application_ip,runtime_application_port)

    app.run(host="127.0.0.1",debug=True,port=3000,threaded=True)
