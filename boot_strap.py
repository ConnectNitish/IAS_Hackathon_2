import os,sys,time
import threading as th

def execute_command(command):
	os.system(command)
	time.sleep(5)

repository_host=sys.argv[1]

list_ports_to_stop = [9000,9939,9935,9932,9931,9930]

for item in list_ports_to_stop:
	item = 'sudo kill -9 $(sudo lsof -t -i:'+str(item)+') &'
	execute_command(item)

list_commnads=['python3 Repository/app.py '+repository_host+' & >> Repo.txt','python3 LoggingModule/Platform_Logger.py '+repository_host+' & >> Logger.txt','python3 requestManager/request_manager.py '+repository_host+' & >> Request_manger.txt','python3 LoadBalancer/LoadBalancer.py '+repository_host+' & >> LB.txt','python3 deployer/app.py '+repository_host+' & >> Deployer.txt','python3 runtime/app.py '+repository_host+'& >> Runtime_App.txt']

for item in list_commnads:
	print(item)
	execute_command(item)



