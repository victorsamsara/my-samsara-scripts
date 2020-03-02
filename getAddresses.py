import json
import requests

"""

+ Add your API Token below

+ This code uses the new Samsara API, check www.samsara.com/api

+ For US customers, baseURL is as follows: https://api.samsara.com/<endpoint>

+ For EU customers, this URL will be: https://api.eu.samsara.com/<endpoint>

"""
access_token = 'yourAPItoken'
baseUrl = 'https://api.samsara.com'

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
	elif response.status_code == 405:
		print(response.text)
		raise ValueError('Method Not Allowed: The API endpoint does not accept that HTTP method')
	elif response.status_code == 429:
		print(response.text)
		raise ValueError('Too Many Requests: Rate limit exceeded ')

	else:
		print(response.text)
		raise ValueError('Request was not successful')

def getAddresses(access_token,_id=None):

	#This function returns the addresses array or a particular address if id is provided

    if _id == None:
        getAddressesURL = '/addresses'
    else:
        getAddressesURL = 'addresses/'+str(_id)

    response = requests.get(baseUrl+getAddressesURL,headers = {'Authorization': 'Bearer '+access_token})
    
    responseCodes(response)
    
    return response.json()['data']

#Sample run
print(getAddresses(access_token,_id))