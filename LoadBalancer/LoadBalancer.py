import os
import sys
import time
import random
import json,requests
from flask import abort
from flask import Flask
from flask import session
from flask import request
from flask import jsonify
from flask import send_file
from flask import redirect, url_for
from flask import render_template

server_config = os.getcwd()+"/LoadBalancer/servers.json"
service_config = os.getcwd()+"/LoadBalancer/services.json"

app = Flask(__name__)

global kafka_IP_plus_port
global load_balancer_ip_port

kafka_IP_plus_port = None
load_balancer_ip_port = None

app.deployment_file_location = 'deployment/to_deploy_folder'
repository_URL = "http://"+sys.argv[1]
    
class LoadBalancer:
    def __init__(self, server_config, service_config):
        self.servers = {}
        self.services = {}

    def load_data(self):
        with open(service_config, 'r') as fp:
            self.services = json.load(fp)
        print(self.services)

    def save_data(self):
        with open(service_config, 'w') as fp:
            json.dump(self.services, fp, indent=4, sort_keys=True)

load_balancer = LoadBalancer(server_config, service_config)

@app.route('/')
def index():
    return 'Inside Load balancer'

@app.route('/register/<module_name>/<machine_ip>/<service_ip>/<service_port>/<machine_port>/<uid>')
def register_services(module_name,machine_ip,service_ip,service_port,machine_port,uid):
    
    print(load_balancer.services)
    try:
        load_balancer.load_data()
        load_balancer.services[uid] = {
        "uid":uid,
        "module_name":module_name,
        "service_ip":service_ip,
        "service_port":service_port,
        "machine_ip":machine_ip,
        "machine_port":machine_port
        }
        print(load_balancer.services)
        load_balancer.save_data()
        return "success"
    except Exception as e:
        print("Error in register_services: ",e)
        return "failure"

@app.route('/get_all_services')
def get_all_services():
    load_balancer.load_data()
    return jsonify(load_balancer.services)

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
    
    global load_balancer_ip_port
    load_balancer_ip_port = get_ip_port("LoadBalancer_Service")
    
    if __debug__:
        print(" load_balancer_ip_port ",load_balancer_ip_port)

def get_ip_and_port(socket):
    ip_port_temp = socket.split(':')
    print(ip_port_temp)
    return ip_port_temp[0],ip_port_temp[1]

if __name__ == '__main__':

    print (' Initiating Load Balancer ')
    get_Server_Configuration()
    lb_ip,lb_port = get_ip_and_port(load_balancer_ip_port)

    if __debug__:
        print("lb_ip,lb_port",lb_ip,lb_port)

    app.run(debug=True, host=lb_ip,port=int(lb_port),threaded=True)
