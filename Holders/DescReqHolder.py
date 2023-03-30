#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Holder for description SDOs
sdoList = ['attack-pattern', 'campaign', 'course-of-action', 'grouping', 'identity', 'indicator', 'infrastructure', 'intrusion-set', 'location', 'malware', 'report', 'threat-actor','vulnerability']

def reqCheck(object):
    if object['type'] in sdoList: 
        try:
            object['description']
        except:
            object['description'] = '???? ???? ???? ???? ???? ???? ???? ???? ???? ????'
            print("     Temporary description property added to " + object['id'])
    return object 
#------------------------------------------------------------------------------

print('Description Req Holder...')

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

#print(bundle)
#print()

for object in bundle['objects']:
    fixed = reqCheck(object)
    object = fixed

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('Description Req Holder...Done')