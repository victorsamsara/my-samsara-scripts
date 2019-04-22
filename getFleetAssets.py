import json
import requests

"""
Add your API Token and groupId below

"""
access_token = 'mdRI3GLBydOLJYXos5TOp7PYdCHRAe'
baseUrl = 'https://api.samsara.com/v1'

def responseCodes(response):

	"""
	This function performs error handling for the API calls.
	"""
	if response.status_code >= 200 and response.status_code < 299:
	#Do nothing, API call was successful
		pass
	elif response.status_code == 400:
		print(response.text)
		raise ValueError('Bad Request: Please make sure the request follows the format specified in the documentation.')
	elif response.status_code == 401:
		print(response.text)
		raise ValueError('Invalid Token: Could not authenticate successfully')
	elif response.status_code == 404:
		print(response.text)
		raise ValueError('Page not found: API Endpoint is invalid')
	else:
		print(response.text)
		raise ValueError('Request was not successful')


def getFleetAssets(access_token):

	#This function returns the assets array in the fleet list JSON
	
	fleetListUrl = '/fleet/assets'
	parameters = {
					"access_token":access_token
				 }
	response = requests.get(baseUrl+fleetListUrl,params=parameters)

	responseCodes(response)

	return response.json()['assets']

#Sample run
print(getFleetAssets(access_token))