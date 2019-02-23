import requests
import json
import csv

"""

This script reads a CSV file with raw addresses and postcodes and prints out another CSV file with the latitude and longitude coordinates for each address and postcode
using the free geocoding service at https://api.postcodes.io/

The above service only works for UK based addresses, however, the script below could be easily adapted to any geocoding service.

"""

url = "https://api.postcodes.io/postcodes"


class addresses_obj():
    
    def __init__(self,address,postcode,latitude='Error',longitude='Error'):
        
        self.address = address
        self.postcode = postcode
        self.latitude = latitude
        self.longitude = longitude
        

        
def read_addresses_csv(addresses_csv):
    
    """
    Format for CSV:
    
    | Address | Postcode | 
    
    """
    
    addresses_obj_list = list()
    
    with open(addresses_csv) as addresses:
        
        addresses_reader = csv.DictReader(addresses)
        for row in addresses_reader:
            
            addresses_obj_list.append(addresses_obj(row['Address'],row['Postcode']))
                  
    return addresses_obj_list



def postcodes_to_latlong(addresses_obj_list):

    """

    This function takes the addresses in object form and returns a postcode dictionary with {"postcode":[latitude,longitude]}

    """

    #Grab postcodes from list of address objects
    post_codes = [ address.postcode for address in addresses_obj_list]
    json_data = {"postcodes":post_codes}

    response = requests.post(url,json=json_data)
    
    result = json.loads(response.text)['result']
    
    #Build dictionary of postcodes with corresponding lat/lon coordinates. If API returns none for a particular postcode, pass
    postcodes_dict = dict()
    for element in result:
        #Don't do anything if API returns None for Postcode
        if element['result'] == None:
            pass
        else:
            postcodes_dict[element['result']['postcode']] = [element['result']['latitude'],element['result']['longitude']]

    return postcodes_dict



def update_latlong_addr_obj(addresses_obj_list,postcode_dict):
    
    #Update address objects with latitude and longitude coordinates for each postcode
    #If API returned 'None' for a postcode, write 'Error, could not find' for that address
    for address in addresses_obj_list:
        
        try:
            address.latitude = postcode_dict[address.postcode][0]
            address.longitude = postcode_dict[address.postcode][1]
        except:
            address.latitude = 'Error, could not find'
            address.longitude = 'Error, could not find'



def postcode_coordinates_csv(addresses_obj_list,name_csv='postcode_coordinates.csv'):

    """

    This function prints a CSV with the following fields:

    | Address | Postcode | Latitude | Longitude |

    """
    
    with open(name_csv,'a') as postcode_coordinates:
        csv_fields = ['Address','Postcode','Latitude','Longitude']
        write_csv = csv.DictWriter(postcode_coordinates,fieldnames=csv_fields)
        write_csv.writeheader()
        
        for obj in addresses_obj_list:
            write_csv.writerow({'Address':obj.address,'Postcode':obj.postcode,'Latitude':obj.latitude,
                                'Longitude':obj.longitude})



#MAIN

addresses_csv = input('Name of Addresses file in CSV format (i.e. addresses.csv): ')
name_csv = input('Name of output file with lat/lon coordinates (i.e. postcode_coordinates.csv: ')

#Read addresses_csv file and convert to addresses object list
addresses_obj_list = read_addresses_csv(addresses_csv)

#Use API to find latitude and longitude coordinates, and return a dictionary with {"postcode":[lat,long]}
postcodes_dict = postcodes_to_latlong(addresses_obj_list)

#Update addresses object list with latitude and longitude coordinates for all addresses
update_latlong_addr_obj(addresses_obj_list,postcodes_dict)

#Output CSV file with Address, Postcode, Latitude and Longitude
postcode_coordinates_csv(addresses_obj_list,name_csv)



