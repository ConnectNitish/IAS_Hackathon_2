from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
import json,requests
import random
import time
import os

server_config = os.getcwd()+"/LoadBalancer/servers.json"
service_config = os.getcwd()+"/LoadBalancer/services.json"
import sys



'''argument_list = sys.argv
kafka_ip = argument_list[1]
ip = argument_list[2]
port = argument_list[3]
host_url = ip + ":" + str(port)

print("kafka_ip ",kafka_ip)
print("host_url ",host_url)'''

class Service:
    def __init__(self, serviceName,serviceInstances):
        self.serviceName = serviceName
        self.serviceInstances = serviceInstances
        
    def addInstance(self, IP, PORT):
        url = IP + ":" + str(PORT)
        if url in self.serviceInstances:
            return False
        self.serviceInstances.append(url)
        return True
    def removeInstance(self, IP, PORT):
        url = IP + ":" + str(PORT)
        self.serviceInstances.remove(url)
    def getServiceName(self):
        return self.serviceName
    def getRunningInstances(self):
        return self.serviceInstances
      
class Server:
    ID = 0
    def __init__(self, serverIP, username, password):
        self.serverID = Server.ID + 1
        self.serverIP = serverIP
        self.username = username
        self.password = password
        self.RAM = 0
        self.CPU = 10
        self.isUp = True
        self.services = []
        Server.ID += 1
    
    def updateStatus(self, val):
        self.isUp = val
    def getAllServices(self):
        return self.services
    def addService(self, serviceName):
        self.services.append(serviceName)
    def removeService(self, serviceName):
        print ("Before removing:", self.services)
        self.services.remove(serviceName)
        for service in self.services:
            if service == serviceName:
                print (service)
                print (type(service))
        print (self.services)
        print ('Removing :', serviceName)
    def updateUtilization(self, RAM, CPU):
        self.RAM = RAM
        self.CPU = CPU
    def getRAM(self):
        return self.RAM
    def getCPU(self):
        return self.CPU
    def getUsername(self):
        return self.username
    def getStatus(self):
        return self.isUp
    def getPassword(self):
        return self.password
    def getServerIP(self):
        return self.serverIP
    
class LoadBalancer:
    def __init__(self, server_config, service_config):
        self.servers = {}
        self.services = {}
        for serverIP in self.read_server_config(server_config):
            ip, portu,username, password = serverIP.split(":")
            print (ip,portu)
            self.servers[ip ] = Server(ip+":"+portu, username, password)
        
        for service_details in self.read_service_config(service_config):
            service_name = service_details["serviceName"]
            instances = service_details["instances"]
            print("in loadbalancer inint")
            print (service_name,instances)
            self.services[service_name] = Service(service_name,instances)

            print(self.services["SchedulingService"].getRunningInstances())
            # self.servers[ip ] = Server(ip+":"+portu, username, password)
        # self.read_service_config(service_config)

    def getAllServices(self):
        result = {}
        result['services'] = []
        # result['servers'] = []
        for service in self.services:
            services_data = {}
            services_data['serviceName'] = self.services[service].getServiceName()
            services_data['instances'] = self.services[service].getRunningInstances()
            result['services'].append(services_data)
            print("services_data",services_data)
        # result['servers'] = self.getAllServers()
        print(self.services)
        return result

    def read_service_config(self, service_config):
        service_data = []
        with open(service_config) as f:
            d = json.load(f )
            print("all servicces are")
            for instance in d['services']:
                service_name = instance['serviceName']
                instances = instance['instances']
                print(service_name)
                print(instances)
                sdetails = {}
                sdetails["serviceName"] = service_name
                sdetails["instances"] = instances
                service_data.append(sdetails)
        return service_data

    def read_server_config(self, server_config):
        server_data = []
        with open(server_config) as f:
            d = json.load(f )
            
            for instance in d['servers']:
                ip = instance['serverIP']
                username = instance['username']
                password = instance['password']
                
                
                val = ip + ":" + username + ":" + password 
                print ("val ",val)
                server_data.append(val)
               
        print("server_data",server_data)
        return server_data

load_balancer = LoadBalancer(server_config, service_config)

from flask import send_file

app = Flask(__name__)

@app.route('/')
def index():
    return 'Load balancer'

@app.route('/register/<module_name>/<ip>/<port>')
def register_services(module_name,ip,port):
    pass



@app.route('/get_all_services')
def get_all_services():
    return jsonify(load_balancer.getAllServices())


global kafka_IP_plus_port
global load_balancer_ip_port

kafka_IP_plus_port = None
load_balancer_ip_port = None

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

    app.run(debug=True, host=lb_ip,port=int(lb_port))
