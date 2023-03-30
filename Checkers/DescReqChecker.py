#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for description SDOs

sdoList = ['attack-pattern', 'campaign', 'course-of-action', 'grouping', 'identity', 'indicator', 'infrastructure', 'intrusion-set', 'location', 'malware', 'report', 'threat-actor','vulnerability']

def reqCheck(object):
    if object['type'] in sdoList:
            
        try:
            object['description']
        except:
            print("    " + object['id'] + " is missing property: description")
     
#------------------------------------------------------------------------------

print('Description Requirement Checker...')

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

print('Description Requirement Checker...Done')