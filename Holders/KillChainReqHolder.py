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
            object['kill_chain_phases'] = [{'kill_chain_name':'unknown','phase_name':'unknown'}]
            print("    Temporary kill_chain_phases property added to " + object['id'])
    return object
     
#------------------------------------------------------------------------------

print('Kill Chain Req Holder...')

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

print('Kill Chain Req Holder...Done')