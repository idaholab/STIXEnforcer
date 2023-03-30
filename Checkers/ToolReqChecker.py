#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in tool SDOs
def reqCheck(object):
    if object['type'] == 'tool':
        try:
            object['labels']
        except:
            print("    " + object['id'] + " is missing property: labels")
    return object        
#------------------------------------------------------------------------------

print('Tool Object Req Checker...')

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

print('Tool Object Req Checker...Done')
