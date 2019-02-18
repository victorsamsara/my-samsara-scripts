import requests
import csv
import json
import copy

base_url = 'https://api.samsara.com/v1/'
access_token = {'mytoken'}

"""

This script creates circular geofences given a CSV file. The CSV file needs to be formatted as follows:

| name | formattedAddress | latitude | longitude | radiusMeters |


Use Case: some customers might need to upload addresses produced by 3rd party systems that do not necessarily include the precise address as seen on google maps. For example, GPS trackers
provide location information on assets based on latitude and longitude only (without a particular address) for dispatchers to go and collect the assets.


API Endpoints used:

/addresses


Conditions: For formatting purposes, the CSV must contain the formattedAddress field, which includes the address as it might be recognized by maps.google.com. However, the circular geofence will be centered 
around the latitude and longitude coordinates only. The formattedAddress does not need to match the latitude and longitude.

"""


def create_addresses_list(addresses_circle_csv):
    
    """
    This function reads a CSV file, discards empty rows,
    and returns an address list with each row in Ordered Dictionary form

    Format for the CSV file:
    ['name','formattedAddress','latitude','longitude','radiusMeters']


    """
    addresses_list = list()
    
    with open(addresses_circle_csv) as addresses:
        
        addresses_reader = csv.DictReader(addresses)
        for row in addresses_reader:
        
            if row['name'] == '':
                #ignore empty rows
                pass
            else:
                #build address list
                addresses_list.append(row)
            
    return addresses_list
    
    

def build_addresses_array(addresses_list):
    
    """
    This function takes the address_list in Ordered Dictionary form

    and builds the address array for the request body in the /addresses endpoint

    """
    
    addresses_array = []
    
    addresses_dict = dict()
    
    
    for item in addresses_list:
        
        #Build addresses array
        addresses_dict['name'] = item['name']
        
        addresses_dict['formattedAddress'] = item['formattedAddress']
        
        #Build circular geofence and add latitue, longitude and radius
        addresses_dict['geofence'] = {'circle':{'latitude':float(item['latitude']),'longitude':float(item['longitude']),'radiusMeters':int(item['radiusMeters'])}}
                                                
        
        #Complete optional fields
        addresses_dict['contactIds'] = []
        addresses_dict['notes'] = ''
        addresses_dict['tagId'] = []
        
        #Append values to address_array
        addresses_array.append(copy.deepcopy(addresses_dict))
        
        #Format Array properly into dictionary in the form {"addresses":Array[...]
        request_body = {"addresses":addresses_array}
        
    return request_body



def post_addresses(access_token,addresses_circle_csv):

    addresses_url = 'addresses'
    
    addresses_list = create_addresses_list(addresses_circle_csv)

    parameters = {
                    "access_token":access_token,
                 }
    
    request_body = build_addresses_array(addresses_list)
    
    addresses_request = requests.post(base_url+addresses_url,params=parameters,json = request_body)
    
    #Returns '200' if successful, for debugging change to return addresses_request.text
    return addresses_request.status_code



addresses_circle_csv = input('Name of Addresses CSV File (inlcude .csv extension): ')
print(post_addresses(access_token,addresses_circle_csv))