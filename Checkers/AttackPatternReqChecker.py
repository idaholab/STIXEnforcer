#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
import re

pattern = '^CAPEC-[0-9]{1,}$'

#Check for elements in object
def reqCheck(object):
    matchFound = False
    
    if object['type'] == 'attack-pattern':
        try:
            temp = object['external_references']
        except:
            print("    " + object['id'] + " is missing entries: external_references")
            return
        
        #Empty external_references list edge case
        if len(temp) == 0:
            print("    " + object['id'] + " is missing properly formatted entries: external_id = CAPEC-???? and/or source_name = 'capec'")
            return object

        for i in range(0,len(temp)):
            if 'external_id' in object['external_references'][i].keys() and 'source_name' in object['external_references'][i].keys() and re.search(pattern, object['external_references'][i]['external_id']) and object['external_references'][i]['source_name'] == 'capec':
                matchFound = True
        
        if matchFound == False:
            print("    " + object['id'] + " is missing properly formatted entries: external_id = CAPEC-???? and/or source_name = 'capec'")    
            
#------------------------------------------------------------------------------

print('AttackPattern Object Requirement Checker...')

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

print('AttackPattern Object Requirement Checker...Done')