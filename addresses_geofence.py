import requests
import csv
import json
import copy

base_url = 'https://api.samsara.com/v1/'
access_token = "yourToken"

"""

This script creates polygonal geofences given a CSV file. The CSV file needs to be formatted as follows:

| name | formattedAddress | notes | lat1 | lon1 | ... | lat30 | lon30 |


Use Case: when migrating from 3rd party systems to Samsara, customers with custom geofences in their address book will
need to import them into Samsara. These 3rd party systems generally allow to export the geofences in CSV format, which
could be easily formatted to use this scripts for automated upload.


API Endpoints used:

/addresses


Conditions: For formatting purposes, the CSV must contain the formattedAddress field, which includes the address as it might be recognized by maps.google.com.
The formattedAddress does not need to match the latitudes and longitudes, as long as the coordinates are in the same geographic location. You could use something
more generic as the formattedAddress, like the State or Country name.

"""


def response_codes(status_code):

    """

    This function performs error handling for the API calls

    """

    if status_code >= 200 and status_code < 299:
        #Do nothing, API call was successful
        pass
    elif status_code == 400:
        raise ValueError('Bad Request: Please make sure the request follows the format specified in the documentation.')
    elif status_code == 401:
        raise ValueError('Invalid Token: Could not authenticate successfully')
    elif status_code == 404:
        raise ValueError('Page not found: API Endpoint is invalid')
    else:
        print(status_code)
        raise ValueError('Request was not successful')



def create_addresses_list(addresses_csv):
    
    """
    This function reads a CSV file, discards empty rows,
    and returns an address list with each row in Ordered Dictionary form

    Format for the CSV file:
    ['name','formattedAddress','notes', lat1','lon1', ... 'lat30','lon30']

    Where lat and lon are vertices for the polygon geofence.

    """
    addresses_list = list()
    
    with open(addresses_csv) as addresses:
        
        addresses_reader = csv.DictReader(addresses)
        for row in addresses_reader:
        
            if row['name'] == '':
                #ignore empty rows
                pass
            else:
                #build address list
                addresses_list.append(row)
            
    return addresses_list
    

    
def build_address_array(addresses_list):
    
    """
    This function pops the first address from the address_list in Ordered Dictionary form

    and builds the address array for the request body in the /addresses endpoint

    """
    
    address_dict = dict()
    vertices_list = list()

    #Pop first address fromm addresses_list
    item = addresses_list.pop(0)
        
    #Build address array
    address_dict['name'] = item['name']
    address_dict['formattedAddress'] = item['formattedAddress']
        
    #Only append vertices with values, discard empty ones.
    if item['lat1'] != '' and item['lon1'] != '':
        vertices_list.append({'latitude':float(item['lat1']),'longitude':float(item['lon1'])})
    
    if item['lat2'] != '' and item['lon2'] != '':
        vertices_list.append({'latitude':float(item['lat2']),'longitude':float(item['lon2'])})
    
    if item['lat3'] != '' and item['lon3'] != '':
        vertices_list.append({'latitude':float(item['lat3']),'longitude':float(item['lon3'])})
    
    if item['lat4'] != '' and item['lon4'] != '':
        vertices_list.append({'latitude':float(item['lat4']),'longitude':float(item['lon4'])})
        
    if item['lat5'] != '' and item['lon5'] != '':
        vertices_list.append({'latitude':float(item['lat5']),'longitude':float(item['lon5'])})
        
    if item['lat6'] != '' and item['lon6'] != '':
        vertices_list.append({'latitude':float(item['lat6']),'longitude':float(item['lon6'])})

    if item['lat7'] != '' and item['lon7'] != '':
        vertices_list.append({'latitude':float(item['lat7']),'longitude':float(item['lon7'])})

    if item['lat8'] != '' and item['lon8'] != '':
        vertices_list.append({'latitude':float(item['lat8']),'longitude':float(item['lon8'])})

    if item['lat9'] != '' and item['lon9'] != '':
        vertices_list.append({'latitude':float(item['lat9']),'longitude':float(item['lon9'])})

    if item['lat10'] != '' and item['lon10'] != '':
        vertices_list.append({'latitude':float(item['lat10']),'longitude':float(item['lon10'])})

    if item['lat11'] != '' and item['lon11'] != '':
        vertices_list.append({'latitude':float(item['lat11']),'longitude':float(item['lon11'])})

    if item['lat12'] != '' and item['lon12'] != '':
        vertices_list.append({'latitude':float(item['lat12']),'longitude':float(item['lon12'])})

    if item['lat12'] != '' and item['lon12'] != '':
        vertices_list.append({'latitude':float(item['lat12']),'longitude':float(item['lon12'])})

    if item['lat13'] != '' and item['lon13'] != '':
        vertices_list.append({'latitude':float(item['lat13']),'longitude':float(item['lon13'])})

    if item['lat14'] != '' and item['lon14'] != '':
        vertices_list.append({'latitude':float(item['lat14']),'longitude':float(item['lon14'])})

    if item['lat15'] != '' and item['lon15'] != '':
        vertices_list.append({'latitude':float(item['lat15']),'longitude':float(item['lon15'])})

    if item['lat16'] != '' and item['lon16'] != '':
        vertices_list.append({'latitude':float(item['lat16']),'longitude':float(item['lon16'])})

    if item['lat17'] != '' and item['lon17'] != '':
        vertices_list.append({'latitude':float(item['lat17']),'longitude':float(item['lon17'])})

    if item['lat18'] != '' and item['lon18'] != '':
        vertices_list.append({'latitude':float(item['lat18']),'longitude':float(item['lon18'])})

    if item['lat19'] != '' and item['lon19'] != '':
        vertices_list.append({'latitude':float(item['lat19']),'longitude':float(item['lon19'])})

    if item['lat20'] != '' and item['lon20'] != '':
        vertices_list.append({'latitude':float(item['lat20']),'longitude':float(item['lon20'])})

    if item['lat21'] != '' and item['lon21'] != '':
        vertices_list.append({'latitude':float(item['lat21']),'longitude':float(item['lon21'])})

    if item['lat22'] != '' and item['lon22'] != '':
        vertices_list.append({'latitude':float(item['lat22']),'longitude':float(item['lon22'])})

    if item['lat23'] != '' and item['lon23'] != '':
        vertices_list.append({'latitude':float(item['lat23']),'longitude':float(item['lon23'])})

    if item['lat24'] != '' and item['lon24'] != '':
        vertices_list.append({'latitude':float(item['lat24']),'longitude':float(item['lon24'])})

    if item['lat25'] != '' and item['lon25'] != '':
        vertices_list.append({'latitude':float(item['lat25']),'longitude':float(item['lon25'])})

    if item['lat26'] != '' and item['lon26'] != '':
        vertices_list.append({'latitude':float(item['lat26']),'longitude':float(item['lon26'])})

    if item['lat27'] != '' and item['lon27'] != '':
        vertices_list.append({'latitude':float(item['lat27']),'longitude':float(item['lon27'])})

    if item['lat28'] != '' and item['lon28'] != '':
        vertices_list.append({'latitude':float(item['lat28']),'longitude':float(item['lon28'])})

    if item['lat29'] != '' and item['lon29'] != '':
        vertices_list.append({'latitude':float(item['lat29']),'longitude':float(item['lon29'])})

    if item['lat30'] != '' and item['lon30'] != '':
        vertices_list.append({'latitude':float(item['lat30']),'longitude':float(item['lon30'])})
    
    #Build geofence and append array of vertices for each address
    address_dict['geofence'] = {'circle':{'latitude':0.0,'longitude':0.0,'radiusMeters':0},
                                            'polygon':{'vertices':vertices_list}}

    #Complete optional fields
    address_dict['notes'] = item['notes']
    address_dict['contactIds'] = []
    address_dict['tagId'] = []

    #Copy address_dict to addresses_array
    address_array = [copy.deepcopy(address_dict)]
        
    return address_array



def post_addresses(access_token,address_array):

    addresses_url = 'addresses'
    
    access_token = {"access_token":access_token}

    request_body = {"addresses":address_array}
    
    response = requests.post(base_url+addresses_url,params=access_token,json=request_body)

    response_codes(response.status_code)

    if response.status_code == 200:
        print('Successful geofence upload: '+ address_array[0]['name'])
    else:
        print('Failed geofence upload: '+ address_array[0]['name'])
        print(response.text)

    return response.json()





#MAIN

#Read CSV and turn into addresses list
addresses_list = create_addresses_list('your_csv_file.csv')

#Loop through addresses list, and upload one at a time
while len(addresses_list) > 0:

    address_array = build_address_array(addresses_list)

    post_addresses(access_token,address_array)







