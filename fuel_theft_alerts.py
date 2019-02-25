import json
import requests
import time
from twilio.rest import Client

"""

The following script provides a mechanism to send an SMS alert if a fuel level anomaly is detected with any of the vehicles.

A fuel level anomaly consists of a big drop in fuel level percent in a short period of time, which could be due to fuel theft.
If fuel is being exctracted from the vehicle's tank, we should expect to see a considerable decrease in the fuel level percent.

The logic of the script is simple. It uses two main parameters that are tunable by the end user:

    1. fuelLevelPercent_threshold: a value between 0.0 and 1.0 that indicates the threshold that we want to alert at. 
    This is not the fuel level but the delta in existing fuel level versus previously recorded fuel level.

    2. time_threshold: the intervals at which we want to measure fuel level percent.

For example, fuelLevelPercent_threshold of 0.2 and time_threshold of 600 seocond (or 10 minutes) means that if the fuel level 
percent changes by 0.2 (current fuel value - previous fuel value) within 10 minutes (which is the interval between API calls),
then this will trigger the SMS alert.


API Endpoints used:

/fleet/list


Special note: this script uses Twilio as the SMS message provider. Free trial account here: https://www.twilio.com/try-twilio  
You will also have to install the Twilio package -> pip install twilio

"""


base_url = 'https://api.samsara.com/v1'


#Samsara account parameters
access_token = {'your_samsara_token'}
groupId = 12334

#The two parameters below specify the thresholds used to determine potential fuel theft
#In this case, we want to alert if the Fuel Level drops by 20% in 10 minutes or less
fuelPercent_threshold = 0.2
time_threshold_sec = 600

#Twilio global settings
account_sid = 'your_twilio_sid'
auth_token = 'your_twilio_token'
from_num = '+001234567890'
to_num = '+001234567890'



class vehicle_obj():
    
    def __init__(self,_id,name,current_fuelLevelPercent=None,previous_fuelLevelPercent=None):
        
        self._id = _id
        self.name = name
        self.current_fuelLevelPercent = current_fuelLevelPercent
        self.previous_fuelLevelPercent = previous_fuelLevelPercent

    def save_fuelLevelPercent(self):

        self.previous_fuelLevelPercent = self.current_fuelLevelPercent

    #This function compares previous fuel level percent with current level, if level has dropped below threshold an SMS alert is generated
    def fuel_anomaly(self):

        if (self.previous_fuelLevelPercent-self.current_fuelLevelPercent) > fuelPercent_threshold:
            body = 'Fuel Level for vehicle '+self.name+' has decreased by '+str(fuelPercent_threshold*100)+'%\n in the last '+str(int(time_threshold_sec/60))+' minutes.'
            twilio_message(to_num,from_num,body)  
        else:
            pass


def twilio_message(to_num,from_num,body):

    #Twilio SMS
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=to_num,from_=from_num,body=body)



def post_fleet_list(access_token,groupId,startingAfter=None,endingBefore=None,limit=None):
    
    #Return the fleet list in dictionary form
    
    fleet_list_url = '/fleet/list'
    parameters = {
        "access_token":access_token,
        "startingAfter":startingAfter,
        "endingBefore":endingBefore,
        "limit":limit
    }
    request_body = {"groupId":groupId}
    response = requests.post(base_url+fleet_list_url,params=parameters,data=json.dumps(request_body))
    
    return json.loads(response.text)


    
def vehicle_list(fleet_list):
    
    #Return a list of vehicle objects
    
    #Grab vehicle list only, disregards other keys
    fleet_list = fleet_list['vehicles']
    
    #Build list of vehicle_obj
    vehicle_obj_list = [ vehicle_obj(vehicles['id'],vehicles['name'],vehicles['fuelLevelPercent']) for vehicles in fleet_list ]
    
    return vehicle_obj_list



#MAIN

while True:

    try:
        #Build fleet
        fleet_list = post_fleet_list(access_token,groupId)
        vehicle_obj_list = vehicle_list(fleet_list)

        #Create list of vehicles that do report fuel data, ignore vehicles without fuel data
        #Ignore vehicles with fuelLevelPercent = None, and save current_fuelLevelPercent as previous_fuelLevelPercent in fuel_vehicle_obj_list
        fuel_vehicle_obj_list = list()
        for vehicle in vehicle_obj_list:
            if vehicle.current_fuelLevelPercent != None:
                fuel_vehicle_obj_list.append(vehicle)
                vehicle.save_fuelLevelPercent()
            else:
                pass

        #Wait for time threshold until next API call
        time.sleep(time_threshold_sec)

        #Build fleet  again
        fleet_list = post_fleet_list(access_token,groupId)
        current_vehicle_obj_list = vehicle_list(fleet_list)

        #Create list of vehicles that do report fuel data, ignore vehicles without fuel data
        #Ignore vehicles with fuelLevelPercent = None, and save current_fuelLevelPercent as previous_fuelLevelPercent in fuel_vehicle_obj_list
        current_fuel_vehicle_obj_list = list()
        for vehicle in current_vehicle_obj_list:
            if vehicle.current_fuelLevelPercent != None:
                current_fuel_vehicle_obj_list.append(vehicle)
            else:
                pass

        #Update current fuelLevelPercent in original fuel_vehicle_obj_list with most recent data from current_fuel_vehicle_obj_list
        for vehicle1 in fuel_vehicle_obj_list:
            for vehicle2 in current_fuel_vehicle_obj_list:
                if vehicle1._id == vehicle2._id:
                    vehicle1.current_fuelLevelPercent = vehicle2.current_fuelLevelPercent
                else:
                    pass

        #Compare previous and current fuelLevelPercent for each vehicle, and send SMS alert if anomaly detected
        for vehicle in fuel_vehicle_obj_list:
            vehicle.fuel_anomaly()

    except KeyboardInterrupt:
        print('Fuel Theft Alerts finished running')






