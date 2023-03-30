#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for name SDOs

sdoList = ['grouping', 'indicator', 'location', 'malware', 'file']

def reqCheck(object):
    if object['type'] in sdoList:
        try:
            object['name']
        except:
            object['name'] = '????'
            print("    Temporary name property added to " + object['id'])
    return object
#------------------------------------------------------------------------------

print('Name Req Holder...')

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

print('Name Req Holder...Done')