import json
import requests
import datetime

base_url = 'https://api.samsara.com/v1'

access_token = {'r2wbEAP2HmQukCwNDmFGNhAVa0JfBM'}
groupId = 20477

def get_fleet_drivers(access_token,groupId):

	fleet_drivers_url = '/fleet/drivers'
	parameters = {"access_token":access_token}
	request_body = {"groupId":groupId}
	response = requests.get(base_url+fleet_drivers_url,params=parameters,data=json.dumps(request_body))

	return json.loads(response.text)

print(get_fleet_drivers(access_token,groupId))


