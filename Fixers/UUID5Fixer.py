#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
import uuid

oldNewUUIDdict = {}

scoDict = {
    "artifact": ["hashes", "payload_bin"],
    "autonomous-system": ["number"],
    "directory": ["path"],
    "domain-name": ["value"],
    "email-addr": ["value"],
    "email-message": ["from_ref", "subject", "body"],
    "file": ["hashes", "name", "extensions", "parent_directory_ref"],
    "ipv4-addr": ["value"],
    "ipv6-addr": ["value"],
    "mac-addr": ["value"],
    "mutex": ["name"],
    "network-traffic": ["start", "end", "src_ref", "dst_ref", "src_port", "dst_port", "protocols", "extensions"],
    "software": ["name", "cpe", "swid", "languages", "vendor", "version"],
    "url": ["value"],
    "user-account": ["account_type", "user_id", "account_login"],
    "windows-registry-key": ["key", "values"],
    "x509-certificate": ["hashes", "serial_number"]
}
 
SCO_DET_ID_NAMESPACE = uuid.UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")
 
#Update UUIDs and (Save Old, New Pair)
def updateUUIDs(object):
    
    if object['type'] in scoDict.keys():
        #Get current id/uuid
        oldUUID = object['id'].split('--')[1]
        
        #generate contribString from contrib params
        contribList = scoDict[object['type']]
        contribStringDict = {}
        for i in range(len(contribList)):
            try:
                if contribList[i] == "hashes":
                    contribStringDict[contribList[i]] = _choose_one_hash(eval("object['" + contribList[i] + "']"))
                else:
                    contribStringDict[contribList[i]] = eval("object['" + contribList[i] + "']")
            except:
                pass
        
        #Make no changes if not contributing factors
        if len(contribStringDict) == 0:
            return object
        
        newUUID = uuid.uuid5(SCO_DET_ID_NAMESPACE, json.dumps(contribStringDict))
        
        #update uuid
        object['id'] = object['type'].split('--')[0] + '--' + str(newUUID)
        #save old and new uuid in dictionary
        oldNewUUIDdict.update({oldUUID: str(newUUID)})
        
        #return updated object
        return object
    else: #Do Nothing
        return object

#Function stolen fron STIX2 API base.py
def _choose_one_hash(hash_dict):
    if "MD5" in hash_dict:
        return {"MD5": hash_dict["MD5"]}
    elif "SHA-1" in hash_dict:
        return {"SHA-1": hash_dict["SHA-1"]}
    elif "SHA-256" in hash_dict:
        return {"SHA-256": hash_dict["SHA-256"]}
    elif "SHA-512" in hash_dict:
        return {"SHA-512": hash_dict["SHA-512"]}
    else:
        k = next(iter(hash_dict), None)
        if k is not None:
            return {k: hash_dict[k]}

    return None

def dict_replace_value(d, pairsDict):
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v, pairsDict)
        elif isinstance(v, list):
            v = list_replace_value(v, pairsDict)
        elif isinstance(v, str):
            for key, value in pairsDict.items():
                v = v.replace(key, value)
        x[k] = v
    return x

def list_replace_value(l, pairsDict):
    x = []
    for e in l:
        if isinstance(e, list):
            e = list_replace_value(e, pairsDict)
        elif isinstance(e, dict):
            e = dict_replace_value(e, pairsDict)
        elif isinstance(e, str):
            for key, value in pairsDict.items():
                e = e.replace(key, value)
        x.append(e)
    return x

#------------------------------------------------------------------------------

#Startup
print('UUID5 Fixer...')

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
   
#with open(bundle_input, 'r') as f:
#    bundle = json.load(f)
    
#Fix UUID5s
for object in bundle['objects']:
    fixed = updateUUIDs(object)
    object = fixed #Replace old object with new object
#Find and Replace
bundleNew = dict_replace_value(bundle, oldNewUUIDdict)

#Fix UUID5s Second Iteration
for object in bundleNew['objects']:
    fixed = updateUUIDs(object)
    object = fixed #Replace old object with new object
#Find and Replace
bundleNew2 = dict_replace_value(bundleNew, oldNewUUIDdict)

#Convuluted Printing Section
pairs = {}
firstList = []
secondList = []
for item in oldNewUUIDdict.keys():
    if item != oldNewUUIDdict[item]:
        pairs[item] = oldNewUUIDdict[item]
for key in pairs.keys():
    if pairs[key] in pairs.keys():
        firstList.append(key)
        secondList.append(pairs[pairs[key]])        
for key in pairs.keys():
    if key not in firstList and pairs[key] not in secondList:
        firstList.append(key)
        secondList.append(pairs[key]) 
for i in range(0,len(firstList)):
    print('    Renamed ' + firstList[i] + ' to ' + secondList[i])

#Delete json bundle
#os.remove(bundle_input) #ATTN: may be important. we shall see. Actually, it removes the file, so let's avoid that one

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundleNew2))
outFile.close()

print('UUID5 Fixer...Done') 
