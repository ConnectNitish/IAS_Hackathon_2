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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Invalid argument format\n Correct usage:python3 [filename][IP Address][Port Number]")
        exit()
    server_IP,server_port = str(sys.argv[1]),str(sys.argv[2])
    server_id = server_IP+":"+server_port
    obj_Server = Platform_Logger()
    topic_name_list = ["Logging","Request_Manager"]
    obj_Server.initiate_logging(topic_name_list,server_id)
