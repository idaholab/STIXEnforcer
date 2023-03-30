#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json

#Holder Description Length
def descCheck(object):
    for element in object.keys():
        if element == 'description':
            if len(object[element].split()) < 10:
                for i in range(1,11-len(object[element].split())):
                    object[element] += ' ????'
                print("    " + object['id'] + " description temporarily buffered.")
    return object
 
#------------------------------------------------------------------------------

print('Decription Length Holder...')

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
    fixed = descCheck(object)
    object = fixed

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('Description Length Holder...Done')