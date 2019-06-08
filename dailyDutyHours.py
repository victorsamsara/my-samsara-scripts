import json
import requests
import datetime
import csv

"""

This script computes hours between first trip and last trip of the day for hours of duty purposes, including end of 24-hour shift. It produces a CSV file
with the following fields:

| Input Date | Vehicle Name | Start Time | Start Location | End Time | End Location | Total Duty Hours | End of 24-hour Cycle |


Use Case: Some companies that are tachograph or HoS exempt pay their drivers based on "duty hours" on a specific day or 24-hour cycle. 
They would simply run a report to compute how many hours a particular vehicle spent working on a daily basis. This figure can be computed by 
capturing when a vehicle first went on a trip, and when the last trip of the 24-hour cycle ended.


API Endpoints used:

/fleet/list

/fleet/trips


Script flow:

1) Ask user for an input date
2) Get vehicle list, build list of vehicle objects
4) Pull trips for each vehicle for a 24-hour period on the date specified by the user, discard vehicles with empty trips.
5) Add trips to vehicle objects
6) Calculate total duty hours by subtracting end of last trip minus begining of first trip
7) Compute end of shift by adding 24 hours to the start time of the first trip
7) Ask user for CSV file name, and output file.


Considerations: at the moment this script only produces vehicle-specific results, not driver-based.


"""


baseUrl = 'https://api.samsara.com/v1'
access_token = 'mytoken'
groupId = 12345


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
    
    def __init__(self,_id,name,trips = None,first=None,last=None,endShiftMs=None,deltaHours=None):
        
        self._id = _id
        self.name = name
        self.trips = trips
        self.first = first
        self.last = last
        self.endShiftMs = endShiftMs
        self.deltaHours = deltaHours
        
    def calculations(self):
        
        #Discard empty trips
        if not self.trips:
            pass
        #Grab first and last trip for vehicle, compute delta hours between first and last trip
        else:
            self.first = self.trips[0]
            self.last = self.trips[-1]
            self.deltaHours = (self.last['endMs'] - self.first['startMs'])/3600000
            self.deltaHours = round(self.deltaHours,2)



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



def getFleetList(access_token,groupId,startingAfter=None,endingBefore=None,limit=None):

    #This function returns the vehicles array in the fleet list JSON 
    
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
    
    #Return a list of vehicle objects
    
    #Build list of vehicleObj
    vehicleObjList = [ vehicleObj(vehicles['id'],vehicles['name']) for vehicles in fleetList ]
    
    return vehicleObjList



def getFleetTrips(access_token,groupId,vehicleId,startMs,endMs):
    
    tripsUrl = '/fleet/trips'
    parameters = {
        "access_token":access_token,
        "groupId":groupId,
        "vehicleId":vehicleId,
        "startMs":startMs,
        "endMs":endMs
        }
    
    response = requests.get(baseUrl+tripsUrl,params=parameters)
    
    return response.json()['trips']



def addTrips(vehicleObjList,access_token,groupId,startMs,endMs):

    print('Pulling trips: running...')
    #Add trips to the vehicle object "trips" attribute
    for vehicle in vehicleObjList:
        
        #Compute endShiftMs (firstTripStartMs + 24 hours in epochMs) and store in vehicleObj
        firstTripStartMs = getFleetTrips(access_token,groupId,vehicle._id,startMs,endMs)[0]['startMs']
        vehicle.endShiftMs = firstTripStartMs + 86400000

        #Populate trips for each object, endShiftMs is 24 hours after first trip
        vehicle.trips = getFleetTrips(access_token,groupId,vehicle._id,startMs,endMs)
        
        #Run calculations function within vehicleObj
        vehicle.calculations()
    print('Pulling trips: complete!')

    
    
        
def msToDatetime(timestampMs):
    
    timestamp = timestampMs/1000
    dateTime = datetime.datetime.fromtimestamp(timestamp)

    return dateTime    



def createDutyHours(fleetList,nameCSV='duty_hours.csv'):

    #Create CSV for Duty Hours trips

    with open(nameCSV,'a') as dutyHours:
        csvFields = ['Input Date','Vehicle Name','First Trip Start Time','Start Location','Last Trip End Time','End Location','Total Duty Hours','End of 24-hour Cycle']
        writeTrips = csv.DictWriter(dutyHours,fieldnames=csvFields)
        writeTrips.writeheader()
        print('Creating CSV file: running...')
        for vehicle in fleetList:
            #Discard vehicles with no trips
            if len(vehicle.trips) < 1:
                pass
            else:
                writeTrips.writerow({'Input Date':startDt.day+'/'+startDt.month+'/'+startDt.year,
                    'Vehicle Name':vehicle.name,
                    'First Trip Start Time': str(msToDatetime(vehicle.first['startMs']).hour)+':'+str(msToDatetime(vehicle.first['startMs']).minute),
                    'Start Location':vehicle.first['startLocation'],
                    'Last Trip End Time':str(msToDatetime(vehicle.last['endMs']).hour)+':'+str(msToDatetime(vehicle.last['endMs']).minute),
                    'End Location':vehicle.last['endLocation'],
                    'Total Duty Hours':vehicle.deltaHours,
                    'End of 24-hour Cycle':str(msToDatetime(vehicle.endShiftMs).day)+'/'+str(msToDatetime(vehicle.endShiftMs).month)+
                    '/'+str(msToDatetime(vehicle.endShiftMs).year)+' '+str(msToDatetime(vehicle.endShiftMs).hour)+
                    ':'+str(msToDatetime(vehicle.endShiftMs).minute)})
        print('Creating CSV file: complete!')


#MAIN

#Initialize time, after user selects a day the rest of the fields are populated to account for the entire 24hrs
startDt = datetimeObj()
endDt = datetimeObj()
startDt.day,startDt.month,startDt.year = input('Enter Date in day/month/year format (i.e. 18/1/2019): ').split('/')
endDt.day,endDt.month,endDt.year = startDt.day,startDt.month,startDt.year

#Hardcode hour/min for 24hr 
startDt.hour,startDt.minute = 0,0
endDt.hour,endDt.minute = 23,59

#Compute epoch in ms
startDt.computeEpochMs()
endDt.computeEpochMs()

#Get list of vehicles and convert to objects
fleetList = vehicleList(getFleetList(access_token,groupId))

#Add trips to each vehicle object and compute first/last trip and hours in between
addTrips(fleetList,access_token,groupId,startDt.epochMs,endDt.epochMs)

#Output CSV
nameCSV = input('Provide CSV name in format "name.csv" : ')
createDutyHours(fleetList,nameCSV)



                                  



















