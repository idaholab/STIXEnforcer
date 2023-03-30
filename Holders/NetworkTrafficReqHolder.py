#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Check for elements in network-traffic object
def reqCheck(object):
    if object['type'] == 'network-traffic':
        try:
            object['src_port']
        except:
            object['src_port'] = '0'
            print("    Temporary src_port property added to " + object['id'])
            
        try:
            object['dst_port']
        except:
            object['dst_port'] = '0'
            print("    Temporary dst_port property added to " + object['id'])
    return object
#------------------------------------------------------------------------------

print('Network Traffic Req Holder...')

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
    
print('Network Traffic Req Holder...Done')