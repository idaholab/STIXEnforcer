#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in network-traffic object
def reqCheck(object):
    if object['type'] == 'network-traffic':
        try:
            object['src_port']
        except:
            print("    " + object['id'] + " is missing property: src_port")
            
        try:
            object['dst_port']
        except:
            print("    " + object['id'] + " is missing property: dst_port")
#------------------------------------------------------------------------------

print('Network Traffic Object Requirement Checker...')

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
    
print('Network Traffic Object Requirement Checker...Done')