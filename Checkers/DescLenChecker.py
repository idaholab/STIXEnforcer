#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check Description Length
def descCheck(object):
    for element in object.keys():
        if element == 'description':
            if len(object[element].split()) < 10:
                print("    " + object['id'] + " description is too short.")
 
#------------------------------------------------------------------------------

print('Decription Length Requirement Checker...')

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
    descCheck(object)

print('Description Length Requirement Checker...Done')