#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
import re

pattern = '^CAPEC-[0-9]{1,}$'

#Check for elements in object
def reqCheck(object):
    if object['type'] == 'attack-pattern':
        try:
            temp = object['external_references']
        except:
            object['external_references'] = [{'source_name':'capec','external_id':'CAPEC-9999'}]
            print("    Temporary external_references property and entries added to " + object['id'])
            return object
            
        #Empty external_references list edge case
        if len(temp) == 0:
            object['external_references'] = [{'source_name':'capec','external_id':'CAPEC-9999'}]
            print("    Temporary external_references property and entries added to " + object['id'])
            return object
            
        fixed = False
        
        for i in range(0,len(temp)):
            #Missing external_id
            if 'external_id' in object['external_references'][i].keys() and re.search(pattern, object['external_references'][i]['external_id']):
                if 'source_name' in object['external_references'][i].keys() and object['external_references'][i]['source_name'] != 'capec':
                    object['external_references'][i]['source_name'] = 'capec'
                    print("    Temporary source_name property added to " + object['id'] + ' : external_references[' + str(i) + ']')
                    fixed = True
            
            #Missing source_name
            if 'source_name' in object['external_references'][i].keys() and object['external_references'][i]['source_name'] == 'capec':
                if 'external_id' in object['external_references'][i].keys() and not re.search(pattern, object['external_references'][i]['external_id']):
                    object['external_references'][i]['external_id'] = 'CAPEC-9999'
                    print("    Temporary external_id property added to " + object['id'] + ' : external_references[' + str(i) + ']')
                    fixed = True
            
            #Correct Already
            if 'source_name' in object['external_references'][i].keys() and object['external_references'][i]['source_name'] == 'capec':
                if 'external_id' in object['external_references'][i].keys() and re.search(pattern, object['external_references'][i]['external_id']):
                    fixed = True
            
        if fixed == False:
            object['external_references'].append({'source_name':'capec','external_id':'CAPEC-9999'})
            print("    Temporary external_references property and entries added to " + object['id'])
            
    return object      
#------------------------------------------------------------------------------

print('AttackPattern Object Req Holder...')

#Check arguments
try:
    bundle_input = sys.argv[1]
    bundle_output = sys.argv[2]
    bundleCheck = sys.argv[3]
except:
    print('Argument Missing')
    sys.exit()
 
#Load json files
if bundleCheck == "0":
    with open(bundle_input, 'r', encoding='utf-8', errors='replace') as f:
        bundle = json.load(f)
else:
    with open(bundle_output, 'r', encoding='utf-8', errors='replace') as f:
        bundle = json.load(f)

for object in bundle['objects']:
    fixed = reqCheck(object)
    object = fixed
    
#Delete json bundle
#os.remove(bundle_input)

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('AttackPattern Object Req Holder...Done')