# IAS_Hackathon_2

For Kafka Server : 
------------------
1. Navigate to respective Kafka Folder 

2. To run zookepper
<br />
>bin/zookeeper-server-start.sh config/zookeeper.properties

3.To run Kafka
<br />
>bin/kafka-server-start.sh config/server.properties

------------------------------

Setting Up Docker :

<br />
>curl -fsSL https://get.docker.com -o get-docker.sh
<br />
>sudo sh get-docker.sh




------------------------------


For Running Request Manger.py 

python3 requestManager/request_manager.py a b c d 127.0.0.1:9092


For Making Up Logging File 

python3 LoggingModule/Platform_Logger.py 127.0.0.1 9092




