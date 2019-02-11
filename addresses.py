import requests
import csv
import json
import copy

base_url = 'https://api.samsara.com/v1/'
access_token = {"access_token":"LLCbprRKMbfEabEvlX3JAnKxCZLvTV"}



def create_addresses_list(addresses_csv):
    
    """
    This function reads a CSV file, discards empty rows,
    and returns an address list with each row in Ordered Dictionary form

    Format for the CSV file:
    ['name','formattedAddress','lat1','lon1', ... 'lat10','lon10']

    Where lat and lon are vertices for polygon geofence.

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
    
    
def build_addresses_array(addresses_list):
    
    """
    This function takes the address_list in Ordered Dictionary form

    and builds the address array for the request body in the /addresses end point

    """
    
    addresses_array = []
    
    addresses_dict = dict()
    
    vertices_list = list()
    
    
    for item in addresses_list:
        
        #Build address array
        addresses_dict['name'] = item['name']
        
        addresses_dict['formattedAddress'] = item['formattedAddress']
        
        #Discard empty vertices
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
    
        #Build geofence and append array of vertices for each address
        addresses_dict['geofence'] = {'circle':{'latitude':0.0,'longitude':0.0,'radiusMeters':0},
                                                'polygon':{'vertices':vertices_list}}
        
        #Complete optional fields
        addresses_dict['contactIds'] = []
        addresses_dict['notes'] = ''
        addresses_dict['tagId'] = []
        
        #Append values to address_array
        addresses_array.append(copy.deepcopy(addresses_dict))
        
        #Format Array properly into dictionary in the form {"addresses":Array[...]
        request_body = {"addresses":addresses_array}
        
    return request_body


def post_address(access_token,addresses_csv):

    addresses_url = 'addresses'
    
    addresses_list = create_addresses_list(addresses_csv)
    
    request_body = build_addresses_array(addresses_list)
    
    addresses_request = requests.post(base_url+addresses_url,params=access_token,json = request_body)

    return addresses_request.status_code

x = post_address(access_token,'addresses_csv.csv')
print(x)


