import json
import requests

"""
Add your API Token and groupId below

"""
access_token = {'your_token'}
groupId = 1234
base_url = 'https://api.samsara.com/v1'

def response_codes(status_code):

	"""

	This function performs error handling for the API calls

	"""

    if status_code >= 200 and status_code < 299:
    	#Do nothing, API call was successful
    	pass
    elif status_code == 400:
    	raise ValueError('Bad Request: Please make sure the request follows the format specified in the documentation.')
    elif status_code == 401:
    	raise ValueError('Invalid Token: Could not authenticate successfully')
    elif status_code == 404:
		raise ValueError('Page not found: API Endpoint is invalid')
	else:
		print(status_code)
		raise ValueError('Request was not successful')


def post_fleet_list(access_token,groupId,startingAfter=None,endingBefore=None,limit=None):

	#This function returns the vehicles dictionary in the fleet list
	
	fleet_list_url = '/fleet/list'
	parameters = {
					"access_token":access_token,
					"startingAfter":startingAfter,
					"endingBefore":endingBefore,
					"limit":limit
				 }
	request_body = {"groupId":groupId}
	response = requests.post(base_url+fleet_list_url,params=parameters,json=request_body)

	response_codes(response.status_code)

	return response.json()['vehicles']

#Sample run
vehicles = post_fleet_list(access_token,groupId)


