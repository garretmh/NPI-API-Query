# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 12:22:31 2020

@author: Robert Schuldt

Identifying the NPI numeber and names of nursing homes so I am able to 
identify their CCN number from other file sources. There is an API that
I can use from the NPPES NPI Registery to get information on my nursing homes
that I need for this project 
"""

#Initial packages I will need to create the api request and dump into json
import config
import datetime
import requests
import pandas as pd



ts = datetime.datetime.now().isoformat()

print(ts)

npi_file = config.npi_file
npi = pd.read_excel(npi_file, header = None)
#Want to give my column a legible name 
npi.columns = ['npi']


#make my empy json to dump information into
#This actually ended up being a nasy list of dicts of discts
npi_json = []



#Making my column names
cols = ['NPI', 'Organization Name', 'zipcode', 'state']     
organization_name = pd.DataFrame( columns = cols) 


#I will iterate thru the entire list and dump them into a csv file 
print("With dataframe :\n npi")
print("\nIterating over rows using index attribute :\n")
for num in npi['npi']:
    api = "https://npiregistry.cms.hhs.gov/api/?number="+str(num)+"&enumeration_type=&organization_name=&state=&country_code=&limit=&skip=&version=2.0"
    pulled_data = requests.get(api)
    if pulled_data.status_code == 200:
        print("Sucessful Query of API "+ str( num))
        source = pulled_data.json()


        for key in source.keys():
            if key == 'result_count':
                continue
            elif key == 'Errors':
                pass
            elif source['result_count'] == 0:
                pass
    
   
            else:
                number = source['results'][0]['number']
                org_name = source['results'][0]['basic']['name']
                zipcode = source['results'][0]['addresses'][1]['postal_code']
                state = source['results'][0]['addresses'][1]['state']
                organization_name  = organization_name.append({'NPI': number, 'Organization Name': org_name, 'zipcode': zipcode, 'state':state}, ignore_index = True)   
   
        
    else:
        print("ERROR CONTACTING API")
   
organization_name.to_csv(config.output_file)



