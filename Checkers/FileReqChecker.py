#Copyright 2023, Battelle Energy Alliance, LLC

import sys, json

#Check for hash in file object
def reqCheck(object):
    if object['type'] == 'file':
        try:
            object['hashes']
        except:
            print("    " + object['id'] + " is missing property: hashes")    
    return object
            
#------------------------------------------------------------------------------

print('File Object Requirement Checker...')

#Check arguments
try:
    bundle_input = sys.argv[1]
except:
    print('Usage: python FileRegChecker.py <path to bundle>')
    sys.exit()

#Load json files
with open(bundle_input, 'r', encoding='utf-8', errors='replace') as f:
    bundle = json.load(f)
    
for object in bundle['objects']:
    reqCheck(object)

print('File Object Requirement Checker...Done')  
