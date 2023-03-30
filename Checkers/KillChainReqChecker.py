#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for kill_chain_phases SDOs

sdoList = ['attack-pattern', 'indicator', 'infrastructure', 'malware', 'tool']

def reqCheck(object):
    if object['type'] in sdoList:
            
        try:
            object['kill_chain_phases']
        except:
            print("    " + object['id'] + " is missing property: kill_chain_phases")
     
#------------------------------------------------------------------------------

print('Kill Chain Requirement Checker...')

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

print('Kill Chain Requirement Checker...Done')