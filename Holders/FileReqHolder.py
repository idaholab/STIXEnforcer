#Copyright 2023, Battelle Energy Alliance, LLC


import sys, json

#Check for hash in file object
def reqCheck(object):
    if object['type'] == 'file':
        try:
            object['hashes']
        except:
            object['hashes'] = {'MD5':'00000000000000000000000000000000'}
            print("    Temporary hashes property added to " + object['id'])    
    return object
            
#------------------------------------------------------------------------------

print('File Req Holder...')

#Check arguments
try:
    bundle_input = sys.argv[1]
    bundle_output = sys.argv[2]
    bundleCheck = sys.argv[3]
except:
    print('Usage: python FileRegHolder.py <path to bundle>')
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

print('File Req Holder...Done')  
