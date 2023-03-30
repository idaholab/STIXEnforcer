#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in tool SDOs
def reqCheck(object):
    if object['type'] == 'location':
        try:
            object['region']
        except:
            print("    " + object['id'] + " is missing property: region")
    return object        
#------------------------------------------------------------------------------

print('Location Object Req Checker...')

#Check arguments
try:
    bundle_input = sys.argv[1]
except:
    print('Argument Missing')
    sys.exit()
 
#Load json files
with open(bundle_input, 'r', encoding='utf-8', errors='replace') as f:
    bundle = json.load(f)

for object in bundle['objects']:
    reqCheck(object)

print('Location Object Req Checker...Done')
