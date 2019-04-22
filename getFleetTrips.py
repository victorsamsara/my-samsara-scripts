import json
import requests



access_token = 'yourToken'
baseUrl = 'https://api.samsara.com/v1'
groupId = 'yourGroupId in Integer format'

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



def getFleetTrips(access_token,groupId,vehicleId,startMs,endMs):

	#This function returns the vehicles dictionary in the fleet list
	
	fleetListUrl = '/fleet/trips'
	parameters = {
					"access_token":access_token,
					"endMs":endMs,
					"startMs":startMs,
					"vehicleId":vehicleId
				 }

	response = requests.get(baseUrl+fleetListUrl,params=parameters)

	responseCodes(response)

	return response.json()['trips']

#Sample run
print(getFleetTrips('mdRI3GLBydOLJYXos5TOp7PYdCHRAe',24131,212014918454264,1551892283000,1554570683000))


