#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in software SDOs
def reqCheck(object):
    if object['type'] == 'software':
        try:
            object['cpe']
        except:
            object['cpe'] = 'cpe:2.3:a:b:c:0.0:0:*:*:*:*:*:*'

            print("    Temporary cpe property added to " + object['id'])
            
        try:
            object['version']
        except:
            object['version'] = '0000'
            print("    Temporary version property added to " + object['id'])
            
        try:
            object['vendor']
        except:
            object['vendor'] = '????'
            print("    Temporary vendor property added to " + object['id'])
    return object        
#------------------------------------------------------------------------------

print('Software Object Req Holder...')

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

print('Software Object Req Holder...Done')
