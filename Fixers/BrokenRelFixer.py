#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
import time
import datetime
 
#Remove Broken Relationships
def brokenRelFixer(bundle):

    objectList = []
    delList = []

    for object in bundle['objects']:
        if object['type'] != 'relationship':
            objectList.append(object['id'])
    
    for object in bundle['objects']:
        if object['type'] == 'relationship':
            if (object['source_ref'] in objectList) and (object['target_ref'] in objectList):
                pass
            else:
                delList.append(object)
    
    #Remove object
    for entry in delList:
        #delete object
        bundle['objects'].remove(entry)
    
#------------------------------------------------------------------------------

#Startup
print('Broken Rel Fixer...')

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

brokenRelFixer(bundle)

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('Broken Rel Fixer...Done')
