import requests
import json

base_url = "https://api.samsara.com/v1/fleet/"
access_token = {"access_token":"LLCbprRKMbfEabEvlX3JAnKxCZLvTV"}
groupId = {"groupId":20481}

def add_address(access_token,groupId,name,address,radius):

	add_address_url = "add_address"
	
	json_data = {"groupId":groupId["groupId"],"name":name,"address":address,"radius":radius}

	add_address_request = requests.post(base_url+add_address_url,params=access_token,json = json_data)

	return add_address_request.status_code


x = add_address(access_token,groupId,"Naico2","London, EC2A 1AF",50)

print(x)

