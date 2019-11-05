import json
import requests
import time
from twilio.rest import Client

"""

The following script provides a mechanism to send an SMS alert if a fuel level anomaly is detected with any of the vehicles.

A fuel level anomaly consists of a big drop in fuel level percent in a short period of time, which could be due to fuel theft.
If fuel is being exctracted from the vehicle's tank, we should expect to see a considerable decrease in the fuel level percent.

The logic of the script is simple. It uses two main parameters that are tunable by the end user:

    1. fuelPercentThreshold: a value between 0.0 and 1.0 that indicates the threshold that we want to alert at. 
    This is not the fuel level but the delta in existing fuel level versus previously recorded fuel level.

    2. timeThresholdSec: the intervals at which we want to measure fuel level percent in seconds.

For example, fuelPercentThreshold of 0.2 and timeThresholdSec of 600 seoconds (or 10 minutes) means that if the fuel level 
percent changes by 0.2 (current fuel value - previous fuel value) within 10 minutes (which is the interval between API calls),
then this will trigger the SMS alert.


API Endpoints used:

/fleet/list


Special note: this script uses Twilio as the SMS message provider. Free trial account here: https://www.twilio.com/try-twilio  
You will also have to install the Twilio package -> pip install twilio

"""


baseUrl = 'https://api.samsara.com/v1'


#Samsara account parameters
access_token = 'your_samsara_token'
groupId = 12334

#The two parameters below specify the thresholds used to determine potential fuel theft
#In this case, we want to alert if the Fuel Level drops by 20% in 10 minutes or less
fuelPercentThreshold = 0.2
timeThresholdSec = 600

#Twilio global settings
accountSid = 'your_twilio_sid'
authToken = 'your_twilio_token'
fromNum = '+001234567890'
toNum = '+001234567890'


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


class vehicleObj():
    
    def __init__(self,_id,name,currentFuelLevelPercent=None,previousFuelLevelPercent=None):
        
        self._id = _id
        self.name = name
        self.currentFuelLevelPercent = currentFuelLevelPercent
        self.previousFuelLevelPercent = previousFuelLevelPercent

    def saveFuelLevelPercent(self):

        self.previousFuelLevelPercent = self.currentFuelLevelPercent

    #This function compares previous fuel level percent with current level, if level has dropped below threshold an SMS alert is generated
    def fuelAnomaly(self):

        if self.previousFuelLevelPercent < fuelPercentThreshold:
            #Do nothing if previousFuelLevelPercent is already below threshold (i.e. fuel level is already low)
            pass
        elif (self.previousFuelLevelPercent-self.currentFuelLevelPercent) > fuelPercentThreshold:
            body = 'Fuel Level for vehicle '+self.name+' has decreased by '+str(fuelPercentThreshold*100)+'%\n in the last '+str(int(timeThresholdSec/60))+' minutes.'
            twilio_message(toNum,fromNum,body)  
        else:
            pass


def twilio_message(toNum,fromNum,body):

    #Twilio SMS
    client = Client(accountSid, authToken)
    message = client.messages.create(to=toNum,from_=fromNum,body=body)



def getFleetList(access_token,groupId,startingAfter=None,endingBefore=None,limit=None):

    #This function returns the vehicles dictionary in the fleet list
    
    fleetListUrl = '/fleet/list'
    parameters = {
                    "access_token":access_token,
                    "startingAfter":startingAfter,
                    "endingBefore":endingBefore,
                    "limit":limit
                 }
    requestBody = {"groupId":groupId}
    response = requests.get(baseUrl+fleetListUrl,params=parameters,json=requestBody)

    responseCodes(response)

    return response.json()['vehicles']


    
def vehicleList(fleetList):
    
    #Build list of vehicleObj
    vehicleObj_list = [ vehicleObj(vehicles['id'],vehicles['name'],vehicles['fuelLevelPercent']) for vehicles in fleetList ]
    
    #Return a list of vehicle objects
    return vehicleObj_list



#MAIN

while True:

    try:
        #Build fleet
        fleetList = getFleetList(access_token,groupId)
        vehicleObj_list = vehicleList(fleetList)

        #Create list of vehicles that do report fuel data, ignore vehicles without fuel data
        #Ignore vehicles with fuelLevelPercent = None, and save currentFuelLevelPercent as previousFuelLevelPercent in firstFuelVehicleObj_list
       firstFuelVehicleObj_list = list()
        for vehicle in vehicleObj_list:
            if vehicle.currentFuelLevelPercent != None:
               firstFuelVehicleObj_list.append(vehicle)
                vehicle.saveFuelLevelPercent()
            else:
                pass

        #Wait for time threshold until next API call
        time.sleep(timeThresholdSec)

        #Build fleet  again
        fleetList = getFleetList(access_token,groupId)
        current_vehicleObj_list = vehicleList(fleetList)

        #Create list of vehicles that do report fuel data, ignore vehicles without fuel data
        #Ignore vehicles with fuelLevelPercent = None, and save currentFuelLevelPercent as previousFuelLevelPercent infirstFuelVehicleObj_list
        secondFuelVehicleObj_list = list()
        for vehicle in current_vehicleObj_list:
            if vehicle.currentFuelLevelPercent != None:
                secondFuelVehicleObj_list.append(vehicle)
            else:
                pass

        #Update current fuelLevelPercent in originalfirstFuelVehicleObj_list with most recent data from secondFuelVehicleObj_list
        for vehicle1 in firstFuelVehicleObj_list:
            for vehicle2 in secondFuelVehicleObj_list:
                if vehicle1._id == vehicle2._id:
                    vehicle1.currentFuelLevelPercent = vehicle2.currentFuelLevelPercent
                else:
                    pass

        #Compare previous and current fuelLevelPercent for each vehicle, and send SMS alert if anomaly detected
        for vehicle in firstFuelVehicleObj_list:
            vehicle.fuelAnomaly()

    except KeyboardInterrupt:
        print('Fuel Theft Alerts finished running')






