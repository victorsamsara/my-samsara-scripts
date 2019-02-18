import requests
import csv
import json
import copy

access_token = {'LLCbprRKMbfEabEvlX3JAnKxCZLvTV'}
base_url = 'https://api.samsara.com/v1'
groupId = {"groupId":20481}













dispatch_jobs = {
					"scheduled_arrival_time_ms": 1545325296000,
					"scheduled_departure_time_ms":None,
					"notes": "Ensure crates are stacked no more than 3 high.",
					"destination_name": None,
					"destination_address": "London E3 3GW, UK",
					"destination_address_id":4422740,
					"destination_lat":None,
					"destination_lng":None
				}
				
route_data = {
					"vehicle_id":None,
					"driver_id":None,
					"actual_start_ms":None,
					"actual_end_ms":None,
					"scheduled_start_ms": 1545238896000,
					"scheduled_end_ms": 1545411696000,
					"name": "Bid #123",
					"group_id":None,
					"start_location_name": "King's Cross St Pancras",
					"start_location_address": "Euston Rd, Kings Cross, London N1C 4QP, UK",
					"start_location_address_id":4422741,
					"start_location_lat":None,
					"start_location_lng":None
				}


def pretty_json_print(json_text):

    print(json.dumps(json.loads(json_text),indent=4))

    

def create_address_list(addresses_csv):
    
    """
    This function reads a CSV file, discards empty rows,
    and returns an address list with each row in Ordered Dictionary form

    Format for the CSV file:
    ['name','formattedAddress','lat1','lon1', ... 'lat6','lon6']

    where lat and lon are vertices for polygon geofence.

    """
    address_list = []
    with open(addresses_csv) as addresses:
    	addresses_reader = csv.DictReader(addresses)
    	for row in addresses_reader:
    		#ignore empty rows
    		if row['name'] == '':
    			pass
    		else:
    			#build address list
    			address_list.append(row)
    return address_list
    
    
def build_address_array(address_list):
    """
    This function takes the address_list in Ordered Dictionary form

    and builds the address array for the request body in the /addresses end point
    """
    
    address_array = []
    address_dict = dict()
    vertices_list = list()
    
    
    for element in address_list:
         #Build address array
        address_dict['name'] = element['name']
        address_dict['formattedAddress'] = element['formattedAddress']
        #Discard empty vertices
        if element['lat1'] != '' and element['lon1'] != '':
            vertices_list.append({'latitude':float(element['lat1']),'longitude':float(element['lon1'])})
        if element['lat2'] != '' and element['lon2'] != '':
            vertices_list.append({'latitude':float(element['lat2']),'longitude':float(element['lon2'])})
        if element['lat3'] != '' and element['lon3'] != '':
            vertices_list.append({'latitude':float(element['lat2']),'longitude':float(element['lon2'])})
        if element['lat4'] != '' and element['lon4'] != '':
            vertices_list.append({'latitude':float(element['lat3']),'longitude':float(element['lon3'])})  
        if element['lat5'] != '' and element['lon5'] != '':
            vertices_list.append({'latitude':float(element['lat4']),'longitude':float(element['lon4'])})  
        if element['lat6'] != '' and element['lon6'] != '':
            vertices_list.append({'latitude':float(element['lat6']),'longitude':float(element['lon6'])})
        if element['lat7'] != '' and element['lon7'] != '':
            vertices_list.append({'latitude':float(element['lat7']),'longitude':float(element['lon7'])})
    
        #Build geofence and append array of vertices for each address, circle is ignored
        address_dict['geofence'] = {'circle':{'latitude':0.0,'longitude':0.0,'radiusMeters':0},'polygon':{'vertices':vertices_list}}
        #Complete optional fields
        address_dict['contactIds'] = []
        address_dict['notes'] = ''
        address_dict['tagId'] = []
        #Append values to address_array using deepcopy
        address_array.append(copy.deepcopy(address_dict))
        #Format Array properly into dictionary in the form {"addresses":Array[...]
        request_body = {"addresses":address_array}
        
    return request_body



def get_dispatch_routes(access_token,groupId,end_time=None,duration=None):

	dispatch_routes_url = '/fleet/dispatch/routes'
	parameters = {
					"access_token":access_token,
					"groupId":groupId,
					"end_time":end_time,
					"duration":duration
				 }
	response = requests.get(base_url+dispatch_routes_url,params=parameters)
	return response.text



#sample = get_dispatch_routes('LLCbprRKMbfEabEvlX3JAnKxCZLvTV',20481)


def post_dispatch_routes(access_token,dispatch_jobs,route_data):

	dispatch_routes_url = '/fleet/dispatch/routes'
	parameters = {
					"access_token":access_token,
				 }
	request_body = route_data
	request_body["dispatch_jobs"] = [dispatch_jobs]
	response = requests.post(base_url+dispatch_routes_url,params=parameters, data=json.dumps(request_body))
	return response.text



#sample = post_dispatch_routes(access_token,dispatch_jobs,route_data)





















def post_addresses(access_token,addresses_csv):

    addresses_url = '/addresses'
    parameters = {
					"access_token":access_token,
				 }
    
    address_list = create_address_list(addresses_csv)
    request_body = build_address_array(address_list)
    address_request = requests.post(base_url+addresses_url,params=parameters,json = request_body)

    return address_request


addresses = post_addresses(access_token,'addresses_csv.csv')

print(addresses)







