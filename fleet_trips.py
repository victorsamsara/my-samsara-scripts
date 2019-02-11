import csv
import json
import requests
import datetime


#access_token = {'rFKSC1iwTJ6Qtp5Cw2PLV294q6vpfv'}
#groupId = 9665
#vehicleId = 212014918171841

base_url = 'https://api.samsara.com/v1'


class datetime_obj():
    
    def __init__(self,year=0,month=0,day=0,hour=0,minute=0,epoch=0,epoch_ms=0):
        
        self.year = year
        self.month = month
        self.hour = hour
        self.day = day
        self.hour = hour
        self.minute = minute
        self.epoch = epoch
        self.epoch_ms = epoch_ms
        
    
    def compute_epoch(self):
        
        self.epoch = (datetime.datetime(int(self.year),int(self.month),int(self.day),int(self.hour),int(self.minute)).timestamp())
        
    def compute_epoch_ms(self):
        
        self.epoch_ms = 1000*(datetime.datetime(int(self.year),int(self.month),int(self.day),int(self.hour),int(self.minute)).timestamp())
        
    def __str__(self):

    	return str(self.year)+'/'+str(self.month)+'/'+str(self.day)+' '+str(self.hour)+':'+str(self.minute)


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

	return response.text


def ms_to_datetime(timestamp_ms):

	timestamp = timestamp_ms/1000
	date_time = datetime.datetime.fromtimestamp(timestamp)

	return date_time

def create_trips_csv(fleet_trips_json,name_csv='trips_csv.csv'):

	"""
	This function takes the response in JSON format from the /fleet/trips end points
	and creates a CSV file with truncated fields as specified in the "fields" array below.

	"""
    #Grab 'trips' dictionary
	trips = json.loads(fleet_trips_json)['trips']

	#Create CSV file
	with open(name_csv,'a') as trips_csv:
		fields = ['startMs','endMs','startLocation','endLocation','distanceMeters','fuelConsumedMl']
		write_trips = csv.DictWriter(trips_csv,fieldnames=fields)
		write_trips.writeheader()
		for items in trips:
			write_trips.writerow({'startMs':ms_to_datetime(items['startMs']),
				'endMs':ms_to_datetime(items['endMs']),
				'startLocation':items['startLocation'],
				'endLocation':items['endLocation'],
				'distanceMeters':items['distanceMeters'],
				'fuelConsumedMl':items['fuelConsumedMl']})

#MAIN

#Instantiate start and end times
start_dt = datetime_obj()
end_dt = datetime_obj()

while True:

	try:
		print('\n')
		access_token = input('Enter access token: ')
		groupId = int(input('Enter groupId: '))
		vehicleId = int(input('Enter vehicleId: '))

		start_dt.day,start_dt.month,start_dt.year = input('Enter Start Date in day/month/year format (i.e: 18/1/2019): ').split('/')
		start_dt.hour,start_dt.minute = input('Enter Start Time in hour:minute format (i.e 15:30): ').split(':')

		end_dt.day,end_dt.month,end_dt.year = input('Enter End Date in day/month/year format (i.e: 25/1/2019): ').split('/')
		end_dt.hour,end_dt.minute = input('Enter End Time in hour:minute (i.e 23:59): ').split(':')

		name_csv = input('Name of CSV file: ')

		#Compute epoch in ms
		start_dt.compute_epoch_ms()
		end_dt.compute_epoch_ms()

		fleet_trips = post_fleet_trips(access_token,groupId,vehicleId,start_dt.epoch_ms,end_dt.epoch_ms)

		create_trips_csv(fleet_trips,name_csv)


	except KeyboardInterrupt:

		print(' Good Bye')
		break





