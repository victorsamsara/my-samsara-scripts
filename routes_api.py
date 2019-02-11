import csv
import json
import requests


access_token = {'access_token':'LLCbprRKMbfEabEvlX3JAnKxCZLvTV'}
base_url = 'https://api.samsara.com/v1/fleet/'
dispatch_routes_url = 'dispatch/routes'


# Open the CSV  
f = open( 'routes_csv.csv', 'r' )  
# Change each fieldname to the appropriate field name. I know, so difficult.  
reader = csv.DictReader( f, fieldnames = ( "scheduled_arrival_time_ms","scheduled_departure_time_ms","notes","destination_name"," destination_address_id","destination_lat","destination_ln" ))  
# Parse the CSV into JSON  
print(json.dumps( [ row for row in reader ] ))  


route_data = {
				"dispatch_jobs": [
									{
										"scheduled_arrival_time_ms": 1462881998034,
										"scheduled_departure_time_ms": 1462881998034,
										"notes": "Ensure crates are stacked no more than 3 high.",
										"destination_name": "ACME Inc. Philadelphia HQ",
										"destination_address": "123 Main St, Philadelphia, PA 19106",
										"destination_address_id": 67890,
										"destination_lat": 123.456,
										"destination_lng": 37.459
									}
								],
				"vehicle_id": 444,
				"driver_id": 555,
				"actual_start_ms": 1462882098000,
				"actual_end_ms": 1462882101000,
				"scheduled_start_ms": 1462881998034,
				"scheduled_end_ms": 1462881998034,
				"name": "Bid #123",
				"group_id": 101,
				"start_location_name": "ACME Inc. Philadelphia HQ",
				"start_location_address": "123 Main St, Philadelphia, PA 19106",
				"start_location_address_id": 67890,
				"start_location_lat": 123.456,
				"start_location_lng": 37.459
			}

"""

with open('routes_csv.csv', 'rU') as routes_csv:
	routes = csv.reader(routes_csv)

	for line in routes:
		print(line)


"""


"""

# import
import json
import requests

# globals
api_url = 'https://api.samsara.com/v1'


# function to call /dispatch/routes
def samsara1():

    endpoint_url = api_url + '/fleet/dispatch/routes'

    # parameters for the request
    my_params = (('access_token', 'foo'),)

    # data to send with the request
    my_data = '''{"dispatch_jobs": [
		{
			"scheduled_arrival_time_ms": 'foo',
			"notes": "Samsara",
			"destination_name": "415",
			"destination_address": "",
			"destination_lat": 37.764330,
			"destination_lng": -122.402724
		},
        {
			"scheduled_arrival_time_ms": 'foo',
			"notes": "Has Many Options",
			"destination_name": "416",
			"destination_address": "444 De Haro San Francisco, CA 94107",
			"destination_lat": 37.760231,
			"destination_lng": -122.402447
        },
        {
            "scheduled_arrival_time_ms": 'foo',
			"notes": "Lets try",
			"destination_name": "417",
			"destination_address": "",
			"destination_lat": 37.754447,
			"destination_lng": -122.393753
        },
        {
            "scheduled_arrival_time_ms": 'foo',
			"notes": "To try them all",
			"destination_name": "418",
			"destination_address": "",
			"destination_lat": 37.754447,
			"destination_lng": -122.393753
        }
	],
	"vehicle_id": 212014918114941,
	"driver_id": null,
	"group_id": null,
	"scheduled_start_ms": 'bar',
	"scheduled_end_ms": 'bar',
	"name": "San Francisco Route 1 - AM",
	"start_location_name": "HQ",
	"start_location_address": "",
	"start_location_lat": 37.764172,
	"start_location_lng": -122.402023
                }'''

    # post request to get the
    resp = requests.post(url = endpoint_url, params = my_params, data = my_data)

def samsara2():

    endpoint_url = api_url + '/fleet/dispatch/routes'

    my_params = (('access_token', 'IFwvJZCB8rbMjq8Vvs4Kmp8p4s09Jz'),)

    my_data = '''{"dispatch_jobs": [
		{
			"scheduled_arrival_time_ms": 1542449739000,
			"notes": "Samsara",
			"destination_name": "419",
			"destination_address": "",
			"destination_lat": 37.764330,
			"destination_lng": -122.402724
		},
        {
			"scheduled_arrival_time_ms": 1542450639000,
			"notes": "Has Many Options",
			"destination_name": "420",
			"destination_address": "'foo'",
			"destination_lat": 37.760231,
			"destination_lng": -122.402447
        },
        {
            "scheduled_arrival_time_ms": 1542451539000,
			"notes": "Lets try ",
			"destination_name": "421,
			"destination_address": "",
			"destination_lat": 37.754447,
			"destination_lng": -122.393753
        },
        {
            "scheduled_arrival_time_ms": 1542452439000,
			"notes": "them all",
			"destination_name": "422",
			"destination_address": "",
			"destination_lat": 37.754447,
			"destination_lng": -122.393753
        }
	],
	"vehicle_id": 212014918322988,
	"driver_id": null,
	"group_id": null,
	"scheduled_start_ms": 1542448839000,
	"scheduled_end_ms": 1542416439000,
	"name": "Route 2",
	"start_location_name": "HQ",
	"start_location_address": "",
	"start_location_lat": 37.764172,
	"start_location_lng": -122.402023
                }'''

    resp = requests.post(url = endpoint_url, params = my_params, data = my_data)

def samsara3():

    endpoint_url = api_url + '/fleet/dispatch/routes'

    my_params = (('access_token', 'IFwvJZCB8rbMjq8Vvs4Kmp8p4s09Jz'),)

    my_data = '''{"dispatch_jobs": [
		{
			"scheduled_arrival_time_ms": 1542474939000,
			"notes": "12 Pallets Milk - D/O",
			"destination_name": "423",
			"destination_address": "",
			"destination_lat": 37.764330,
			"destination_lng": -122.402724
		},
        {
			"scheduled_arrival_time_ms": 1542475839000,
			"notes": "D/O",
			"destination_name": "424",
			"destination_address": "",
			"destination_lat": 37.760231,
			"destination_lng": -122.402447
        },
        {
            "scheduled_arrival_time_ms": 1542476739000,
			"notes": "6 Pallets P/U",
			"destination_name": "425",
			"destination_address": "",
			"destination_lat": 37.754447,
			"destination_lng": -122.393753
        },
        {
            "scheduled_arrival_time_ms": 1542477639000,
			"notes": "Hold overnight - Reefer ON",
			"destination_name": "426",
			"destination_address": "",
			"destination_lat": 37.754447,
			"destination_lng": -122.393753
        }
	],
	"vehicle_id": 212014918114941,
	"driver_id": null,
	"group_id": null,
	"scheduled_start_ms": 1542474039000,
	"scheduled_end_ms": 1542474039000,
	"name": "Route 1 - PM",
	"start_location_name": "HQ",
	"start_location_address": "",
	"start_location_lat": 37.764172,
	"start_location_lng": -122.402023
                }'''

    resp = requests.post(url = endpoint_url, params = my_params, data = my_data)


SF1 = samsara1()
SF2 = samsara2()
SF3 = samsara3()

print("Complete")

"""