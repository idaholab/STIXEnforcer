#Copyright 2023, Battelle Energy Alliance, LLC

import sys
import json
 
#Fix Relationships
def fixRelationship(object):
    relationshipType = {
            'threat-actor.tool':'uses',
            'threat-actor.malware':'uses',
            'threat-actor.attack-pattern':'uses',
            'threat-actor.vulnerability':'targets',
            'threat-actor.identity':'targets,attributed-to,impersonates',
            'threat-actor.threat-actor':'related-to',
            'threat-actor.location':'located-at,targets',
            'threat-actor.intrastructure':'uses,hosts,owns,compromises',
            'course-of-action.indicator':'investigates',
            'course-of-action.attack-pattern':'mitigates',
            'course-of-action.indicator':'mitigates',
            'course-of-action.malware':'mitigates,remediates',
            'course-of-action.tool':'mitigates',
            'course-of-action.vulnerability':'mitigates,remediates',
            'campaign.identity':'targets',
            'campaign.vulnerability':'targets',
            'campaign.tool':'uses',
            'campaign.malware':'uses',
            'campaign.attack-pattern':'uses',
            'campaign.intrusion-set':'attributed-to',
            'campaign.threat-actor':'attributed-to',
            'campaign.intrastructure':'uses,compromises',
            'campaign.location':'targets,originates-from',
            'campaign.campaign':'related-to',
            'attack-pattern.identity':'targets',
            'attack-pattern.location':'targets',
            'attack-pattern.vulnerability':'targets',
            'attack-pattern.tool':'uses',
            'attack-pattern.malware':'uses,delivers',
            'attack-pattern.attack-pattern':'related-to',
            'intrusion-set.threat-actor':'attributed-to',
            'intrusion-set.infrastructure':'uses,hosts,owns,compromises',
            'intrusion-set.location':'targets,originates-from',
            'intrusion-set.identity':'targets',
            'intrusion-set.vulnerability':'targets',
            'intrusion-set.tool':'uses',
            'intrusion-set.malware':'uses',
            'intrusion-set.attack-pattern':'uses',
            'intrusion-set.intrusion-set':'related-to',
            'malware.threat-actor':'authored-by',
            'malware.intrastructure':'uses,targets,exfiltrates-to,beacons-to',
            'malware.ipv4-addr':'communicates-with',
            'malware.ipv6-addr':'communicates-with',
            'malware.domain-name':'communicates-with',
            'malware.url':'communicates-with',
            'malware.identity':'targets',
            'malware.vulnerability':'exploits,targets',
            'malware.location':'targets,originates-from',
            'malware.tool':'uses,drops,downloads',
            'malware.file':'downloads,drops',
            'malware.attack-pattern':'uses',
            'malware.malware':'uses,controls,downloads,drops,variant-of,related-to',
            'malware.intrusion-set':'authored-by',
            'indicator.tool':'indicates',
            'indicator.malware':'indicates',
            'indicator.attack-pattern':'indicates',
            'indicator.campaign':'indicates',
            'indicator.infrastructure':'indicates',
            'indicator.observed-data':'based-on',
            'indicator.intrusion-set':'indicates',
            'indicator.threat-actor':'indicates',
            'indicator.indicator':'related-to',
            'tool.identity':'targets',
            'tool.infrastructure':'uses,targets',
            'tool.vulnerability':'targets',
            'tool.tool':'related-to',
            'tool.malware':'delivers,drops',
            'tool.location':'targets',
            'domain-name.domain-name':'resolves-to',
            'domain-name.ipv4-addr':'resolves-to',
            'domain-name.ipv6-addr':'resolves-to',
            'ipv4-addr.mac-addr':'resolves-to',
            'ipv4-addr.autonomous-system':'belongs-to',
            'ipv6-addr.mac-addr':'resolves-to',
            'ipv6-addr.autonomous-system':'belongs-to',
            'malware-analysis.malware':'characterizes,av-analysis-of,static-analysis-of,dynamic-analysis-of',
            'identity.location':'located-at',
            'infrastructure.infrastructure':'communicates-with,consists-of,uses',
            'infrastructure.ipv4-addr':'communicates-with',
            'infrastructure.ipv6-addr':'communicates-with',
            'infrastructure.domain-name':'communicates-with',
            'infrastructure.url':'communicates-with',
            'infrastructure.observed-data':'consists-of',
            'infrastructure.infrastructure':'controls',
            'infrastructure.malware':'hosts,delivers,controls',
            'infrastructure.tool':'hosts',
            'infrastructure.vulnerability':'has',
            'infrastructure.location':'located-at',
            'vulnerability.threat-actor':'related-to',
            'vulnerability.campaign':'related-to',
            'vulnerability.attack-pattern':'related-to',
            'vulnerability.intrusion-set':'related-to',
            'vulnerability.malware':'related-to',
            'vulnerability.indicator':'related-to',
            'vulnerability.tool':'related-to',
            'vulnerability.vulnerability':'related-to',
            'vulnerability.report':'related-to'} 

    if 'relationship' in object['id']:
        #Extract Relationship
        rel = object['relationship_type']
            
        #Copy target and source from relationship
        src = object['source_ref'].split('--')[0]
        tgt = object['target_ref'].split('--')[0]
            
        #Make Dictionary Key
        key = (src + '.' + tgt)
        yek = (tgt + '.' + src)
            
        #Check if Key is valid
        if (key in relationshipType):
            if(rel in relationshipType[key]):
                return object
            else:
                print('    Changed in ' + object['id'] + ': ' + rel + ' to ' + relationshipType[key].split(',')[0]) #Change rel_type
                object['relationship_type'] = relationshipType[key].split(',')[0]
                object['spec_version'] = '2.1'
                return object
        else:
            if (yek in relationshipType):
                print('    Changed in ' + object['id'] + ': ' + rel + ' to ' + relationshipType[yek].split(',')[0] + ' (swapped src & tgt)') #Swap src and tgt, and change rel_type
                temp_src = object['source_ref']
                temp_tgt = object['target_ref']
                object['source_ref'] = temp_tgt
                object['target_ref'] = temp_src
                object['relationship_type'] = relationshipType[yek].split(',')[0]
                object['spec_version'] = '2.1'
                return object
            else:
                if rel != 'related-to':
                    print('    Changed in ' + object['id'] + ': ' + rel + ' to related-to (default)') #Replace with default relationship type
                object['relationship_type'] = 'related-to'
                object['spec_version'] = '2.1'
                return object
    else:
        return object

#------------------------------------------------------------------------------

#Startup
print('Verb Fixer...')

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

#print(bundle)

for object in bundle['objects']:
    fixed = fixRelationship(object) 
    object = fixed

#print("#######################################")
#print(bundle)    
    
#Delete json bundle
#print(bundle_input)
#os.remove(bundle_input)

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('Verb Fixer...Done')
