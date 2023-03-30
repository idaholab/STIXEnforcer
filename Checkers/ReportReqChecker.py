#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in report SDOs
def reqCheck(object):
    if object['type'] == 'report':
        try:
            object['labels']
        except:
            print("    " + object['id'] + " is missing property: labels")
            
        
        try:
            object['object_refs']
        except:
            print("    " + object['id'] + " is missing property: object_refs")
    return object        
#------------------------------------------------------------------------------

print('Report Object Req Checker...')

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

print('Report Object Req Checker...Done')
