#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
from dateutil.parser import parse
 
typeList = ['infrastructure']
 
#Fix Spec Version
def fixSpecVersion(object):
    if object['type'] in typeList:
        try:
            object['spec_version']
        except:
            object['spec_version'] = "2.1"
            print('    Added spec_version = "2.1" to ' + object['id'])
            
    return object
 
#------------------------------------------------------------------------------

#Startup
print('Spec Version Fixer...')

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
    fixed = fixSpecVersion(object)
    object = fixed

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('Spec Version Fixer...Done')
