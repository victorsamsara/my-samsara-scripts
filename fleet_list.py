import json
import requests



access_token = {'rFKSC1iwTJ6Qtp5Cw2PLV294q6vpfv'}
base_url = 'https://api.samsara.com/v1'
groupId = {"groupId":9665}


def pretty_json_print(json_text):

    print(json.dumps(json.loads(json_text),indent=4))


def post_fleet_list(access_token,groupId,startingAfter=None,endingBefore=None,limit=None):

	#This function returns the fleet list
	
	fleet_list_url = '/fleet/list'
	parameters = {
					"access_token":access_token,
					"startingAfter":startingAfter,
					"endingBefore":endingBefore,
					"limit":limit
				 }
	request_body = groupId
	response = requests.post(base_url+fleet_list_url,params=parameters,data=json.dumps(request_body))
	return response.text


pretty_json_print(post_fleet_list(access_token,groupId))