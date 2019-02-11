import json
import requests
import datetime
import csv

"""

This script computes hours between first trip and last trip of the day for payroll purposes. It produces a CSV file
with the following fields:

| Date | Vehicle Name | Driver | Start Time | Start Location | End Time | End Location | Total Duty Hours |


Use Case: Some companies that are tachograph or HoS exempt pay their drivers based on "duty hours" on a specific day. They would simply run a report to compute
how many hours a particular driver spent working on a daily basis. This figure can be computed by capturing when a vehicle first went on a trip, and when the last trip
of the day ended.


API Endpoints used:

/fleet/list

/fleet/drivers

/fleet/trips


Conditions: Fleet manager must have drivers statically assigned to vehicles on Samsara dashboard for "Driver" column to be populated in CSV file. Otherwise, 
the customer must map vehicle name to drivers after producing the file. 


Script flow:

1) Ask user for a date
2) Get vehicle list, build list of vehicle objects
3) Get drivers, build dictionary with "vehicle id" and "driver name" as key-value pairs for easier parsing
4) Pull trips for each vehicle for a 24-hour period on the date specified by the user, discard vehicles with empty trips.
5) Add trips to vehicle objects
6) Calculate total duty hours by subtracting end of last trip minus begining of first trip
7) Ask user for CSV file name, and output file.


"""




base_url = 'https://api.samsara.com/v1'

access_token = {'mytoken'}
groupId = 12345


class vehicle_obj():
    
    def __init__(self,_id,name,trips = None,first=None,last=None,delta_hours=None):
        
        self._id = _id
        self.name = name
        self.trips = trips
        self.first = first
        self.last = last
        self.delta_hours = delta_hours
        
    def calculations(self):
        
        #Discard empty trips
        if not self.trips:
            pass
        #Grab first and last trip for vehicle, compute delta hours between first and last trip
        else:
            self.first = self.trips[0]
            self.last = self.trips[-1]
            self.delta_hours = (self.last['endMs'] - self.first['startMs'])/3600000
            self.delta_hours = round(self.delta_hours,2)

                

class datetime_obj():
    
    def __init__(self,year=0,month=0,day=0,hour=0,minute=0,epoch_ms=0):
        
        self.year = year
        self.month = month
        self.hour = hour
        self.day = day
        self.hour = hour
        self.minute = minute
        self.epoch_ms = epoch_ms
        
        
    def compute_epoch_ms(self):
        
        self.epoch_ms = 1000*(datetime.datetime(int(self.year),int(self.month),int(self.day),int(self.hour),int(self.minute)).timestamp())
        
    def __str__(self):
        
        return str(self.year)+'/'+str(self.month)+'/'+str(self.day)+' '+str(self.hour)+':'+str(self.minute)


        
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


def get_fleet_drivers(access_token,groupId):

    #Return the driver list in dictionary form

    fleet_drivers_url = '/fleet/drivers'
    parameters = {"access_token":access_token}
    request_body = {"groupId":groupId}
    response = requests.get(base_url+fleet_drivers_url,params=parameters,data=json.dumps(request_body))

    return json.loads(response.text)



def vehicle_list(fleet_list):
    
    #Return a list of vehicle objects
    
    #Grab vehicle list only, disregards other keys
    fleet_list = fleet_list['vehicles']
    
    #Build list of vehicle_obj
    vehicle_obj_list = [ vehicle_obj(vehicles['id'],vehicles['name']) for vehicles in fleet_list ]
    
    return vehicle_obj_list


def convert_driver_dict(drivers):

    #Return a dictionary of 'vehicle id' mapped to driver 'name'

    #Grab 'drivers' key only, disregard other keys
    drivers = drivers['drivers']
    driver_dict = dict()

    for driver in drivers:
        driver_dict[str(driver['vehicleId'])] = driver['name']

    return driver_dict


def post_fleet_trips(access_token,groupId,vehicleId,startMs,endMs):
    
    trips_url = '/fleet/trips'
    parameters = {
        "access_token":access_token
    }
    
    request_body = {
        
        "groupId":groupId,
        "vehicleId":vehicleId,
        "startMs":startMs,
        "endMs":endMs
    }
    
    response = requests.post(base_url+trips_url,params=parameters, data=json.dumps(request_body))
    
    return json.loads(response.text)


def add_trips(vehicle_obj_list,access_token,groupId,startMs,endMs):

    print('Pulling trips: running...')
    #Add trips to the vehicle object "trips" attribute
    for vehicle in vehicle_obj_list:
        
        #Populate trips for each object
        vehicle.trips = post_fleet_trips(access_token,groupId,vehicle._id,startMs,endMs)['trips']
        
        #Run calculations function withi vehicle_obj
        vehicle.calculations()
    print('Pulling trips: complete!')

    
    
        
def ms_to_datetime(timestamp_ms):
    
    timestamp = timestamp_ms/1000
    date_time = datetime.datetime.fromtimestamp(timestamp)

    return date_time    


def create_payroll_trips_csv(fleet_list,driver_dict,name_csv='payroll_trips.csv'):

    #Create CSV for payroll trips

    with open(name_csv,'a') as payroll_trips:
        csv_fields = ['Date','Vehicle Name','Driver','Start Time','Start Location','End Time','End Location','Total Duty Hours']
        write_trips = csv.DictWriter(payroll_trips,fieldnames=csv_fields)
        write_trips.writeheader()
        for vehicle in fleet_list:
            #Discard vehicles with no trips
            if len(vehicle.trips) < 1:
                pass
            else:
                #check if vehicle id has statically assigned driver
                if str(vehicle._id) in driver_dict.keys():
                    write_trips.writerow({'Date':start_dt.day+'/'+start_dt.month+'/'+start_dt.year,
                        'Vehicle Name':vehicle.name,
                        'Driver': driver_dict[str(vehicle._id)],
                        'Start Time': str(ms_to_datetime(vehicle.first['startMs']).hour)+':'+str(ms_to_datetime(vehicle.first['startMs']).minute),
                        'Start Location':vehicle.first['startLocation'],
                        'End Time':str(ms_to_datetime(vehicle.last['endMs']).hour)+':'+str(ms_to_datetime(vehicle.last['endMs']).minute),
                        'End Location':vehicle.last['endLocation'],
                        'Total Duty Hours':vehicle.delta_hours})
                else:
                    write_trips.writerow({'Date':start_dt.day+'/'+start_dt.month+'/'+start_dt.year,
                        'Vehicle Name':vehicle.name,
                        'Driver': 'No driver statically assigned',
                        'Start Time': str(ms_to_datetime(vehicle.first['startMs']).hour)+':'+str(ms_to_datetime(vehicle.first['startMs']).minute),
                        'Start Location':vehicle.first['startLocation'],
                        'End Time':str(ms_to_datetime(vehicle.last['endMs']).hour)+':'+str(ms_to_datetime(vehicle.last['endMs']).minute),
                        'End Location':vehicle.last['endLocation'],
                        'Total Duty Hours':vehicle.delta_hours})



#MAIN

#Initialize time, after user selects a day the rest of the fields are populated to account for the entire 24hrs
start_dt = datetime_obj()
end_dt = datetime_obj()
start_dt.day,start_dt.month,start_dt.year = input('Enter Date in day/month/year format (i.e: 18/1/2019): ').split('/')
end_dt.day,end_dt.month,end_dt.year = start_dt.day,start_dt.month,start_dt.year

#Hardcode hour/min for 24hr 
start_dt.hour,start_dt.minute = 0,0
end_dt.hour,end_dt.minute = 23,59

#Compute epoch in ms
start_dt.compute_epoch_ms()
end_dt.compute_epoch_ms()

#Get list of vehicles and convert to objects
fleet_list = vehicle_list(post_fleet_list(access_token,groupId))

#Get list of drivers and convert to dictionary
drivers = get_fleet_drivers(access_token,groupId)
driver_dict = convert_driver_dict(drivers)

#Add trips to each vehicle object and compute first/last trip and hours in between
add_trips(fleet_list,access_token,groupId,start_dt.epoch_ms,end_dt.epoch_ms)

#Output CSV
name_csv = input('Provide CSV name in format "name.csv" : ')
create_payroll_trips_csv(fleet_list,driver_dict,name_csv)



                                  



















