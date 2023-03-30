#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for name SDOs

sdoList = ['grouping', 'indicator', 'location', 'malware', 'file']

def reqCheck(object):
    if object['type'] in sdoList:
            
        try:
            object['name']
        except:
            print("    " + object['id'] + " is missing property: name")
     
#------------------------------------------------------------------------------

print('Name Requirement Checker...')

#Check arguments
try:
    bundle_input = sys.argv[1]
except:
    print('Argument Missing')
    sys.exit()
 
#Load json files
with open(bundle_input, 'r', encoding='utf-8', errors='replace') as f:
    bundle = json.load(f)

#print(bundle)
#print()

for object in bundle['objects']:
    reqCheck(object)

print('Name Requirement Checker...Done')