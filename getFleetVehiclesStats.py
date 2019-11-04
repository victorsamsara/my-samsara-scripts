import json
import requests
import datetime

"""
Add your API Token and groupId below
"""
access_token = 'yourAPIToken'
baseUrl = 'https://api.samsara.com/v1'

class datetimeObj():
    
    def __init__(self,year=0,month=0,day=0,hour=0,minute=0,epochMs=0):
        
        self.year = year
        self.month = month
        self.hour = hour
        self.day = day
        self.hour = hour
        self.minute = minute
        self.epochMs = epochMs
        
        
    def computeEpochMs(self):
        
        self.epochMs = round(1000*(datetime.datetime(int(self.year),int(self.month),int(self.day),int(self.hour),int(self.minute)).timestamp()))
        
    def __str__(self):
        
        return str(self.year)+'/'+str(self.month)+'/'+str(self.day)+' '+str(self.hour)+':'+str(self.minute)



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



def getFleetVehicleStats(access_token,startMs,endMs,series,tagIds=None,startingAfter=None,endingBefore=None,limit=None):

	#This function returns the vehicles array in the fleet list JSON 
	
	fleetVehicleStatsUrl = '/fleet/vehicles/stats'
	headers = {'Authorization': 'Bearer ' + access_token}
	parameters = {
				    'startMs':startMs.
				    'endMs':endMs,
				    'series':series,
				    'tagId':tagIds,
					'startingAfter':startingAfter,
					'endingBefore':endingBefore,
					'limit':limit
				 }
	response = requests.get(baseUrl+fleetVehicleStatsUrl,headers=header,params=parameters)

	responseCodes(response)

	return response.json()['vehicleStats']