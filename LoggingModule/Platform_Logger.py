import os
import sys
import json
import pickle
import threading as th
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

debug = True

class Platform_Logger:

    def consume_topic(self,function_name,server_id):
        print("---------Consuming Start")
        # consumer = kafka_api_obj.consume_topic(function_name,server_id,server_id)
        consumer = KafkaConsumer(function_name,group_id=server_id,bootstrap_servers=server_id,key_deserializer=lambda m: json.loads(m.decode('utf-8')),value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        print("Consuming End")
        print(consumer)
        for item in consumer:
            print (item)
        print("Final End")

    def initiate_logging(self,topic_name_list,server_id):
        for topic_name in topic_name_list:            
            th.Thread(target=self.consume_topic, args=(topic_name,server_id)).start()



global kafka_IP_plus_port
global logging_ip_port

kafka_IP_plus_port = None
logging_ip_port = None
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
    
    global logging_ip_port
    logging_ip_port = get_ip_port("LoadBalancer_Service")
    
    if __debug__:
        print(" logging_ip_port ",logging_ip_port)

def get_ip_and_port(socket):
    ip_port_temp = socket.split(':')
    print(ip_port_temp)
    return ip_port_temp[0],ip_port_temp[1]

if __name__ == '__main__':

    print (' Initiating Logger ')
    get_Server_Configuration()
    logging_ip,logging_port = get_ip_and_port(kafka_IP_plus_port)

    if __debug__:
        print("logging_ip,logging_port",logging_ip,logging_port)

    obj_Server = Platform_Logger()
    topic_name_list = ["Logging","Request_Manager"]
    obj_Server.initiate_logging(topic_name_list,kafka_IP_plus_port)

    # app.run(debug=True, host=logging_ip,port=int(logging_port))

# if __name__ == '__main__':
#     if len(sys.argv) != 3:
#         print ("Invalid argument format\n Correct usage:python3 [filename][IP Address][Port Number]")
#         exit()
#     server_IP,server_port = str(sys.argv[1]),str(sys.argv[2])
#     server_id = server_IP+":"+server_port
#     obj_Server = Platform_Logger()
#     topic_name_list = ["Logging","Request_Manager"]
#     obj_Server.initiate_logging(topic_name_list,server_id)
