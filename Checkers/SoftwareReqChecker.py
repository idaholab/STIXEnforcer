#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in software SDOs
def reqCheck(object):
    if object['type'] == 'software':
    
        try:
            object['cpe']
        except:
            print("    " + object['id'] + " is missing property: cpe")
            
        try:
            object['version']
        except:
            print("    " + object['id'] + " is missing property: version")
            
        try:
            object['vendor']
        except:
            print("    " + object['id'] + " is missing property: vendor")
            
#------------------------------------------------------------------------------

print('Software Object Requirement Checker...')

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

print('Software Object Requirement Checker...Done')
