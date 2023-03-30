#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
from dateutil.parser import parse
 
timeKeys = ['modified','created','first_seen','last_seen','valid_from','vaild_until','submitted','analysis_started',
'analysis_ended','first_observed','last_observed','published','start_time','stop_time','ctime','mtime','atime',
'date','time_date_stamp','start,end','created_time','account_created','account_expires','credential_last_changed',
'account_first_login','account_last_login','modified_time','validity_not_before','validity_not_after',
'private_key_usage_period_not_before','private_key_usage_period_not_after','object_modified']

def fixTimeFormat(inputTime):
    outputTime = parse(inputTime, fuzzy=True).strftime("%Y-%m-%dT%H:%M:%S.%f")
    outputTime = outputTime[:-3] + 'Z'
    return outputTime
 
#Fix Times
def fixTime(object):
    for element in object.keys():
        if element in timeKeys:
            newTime = fixTimeFormat(object[element])
            if object[element] != newTime:
                print('    Changed in ' + object['id'] + ': ' + object[element] + ' to ' + newTime)
                object[element] = newTime
            
    return object
 
#------------------------------------------------------------------------------

#Startup
print('Time Fixer...')

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
    fixed = fixTime(object)
    object = fixed


outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('Time Fixer...Done')