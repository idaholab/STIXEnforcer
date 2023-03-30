Copyright 2023, Battelle Energy Alliance, LLC
# STIX Enforcer
## Created by Bryan Beckman
### Developed by Will Brant, Zach Priest, and Michael Cutshaw
The STIX Enforcer consists of a series of scripts which when run on a STIX bundle will make various corrections to the bundle for commonly made errors.  These are referred to as “Fixers”.  STIX Enforcer also can check for presence of other “required” (optional in the STIX specification) properties and elements.  This can be considered a stricter STIX validator.  These are referred to as “Checkers”. Additionally, STIX Enforcer can apply place holder values within a bundle for missing properties.  These are referred to as “Holders”. Fixers and Holder modify the inputted STIX bundle, while Checkers only notify the user of missing “required” components.  Each script is designed to be run independently if needed to check or fix a specific property, but are to be run together with the STIX Enforcer.py script

-------
## Usage
+ Download Requirements:
    + pip install -r requirements.txt
+ Run Enforcer
    + python STIX_Enforcer.py [Path to STIX JSON Input Bundle] [Path to STIX JSON Output Bundle] [(optional:) > Path to Printing Output]

**Note:** If only path to one bundle is provided as an argument, then it is considered both the input and the output and file overwriting will occur

## Object Properties
| Object Type | Enforced Properties (Previously Optional) |
|:-----------|----------------------------:| 
|Vulnerability | description, external_references[source_name, external_id, cve] |
|Software | cpe, version, vendor |
|Grouping | name, description |
|Indicator | name, description, kill_chain_phases |
|Location | name, description |
|Malware | name description, kill_chain_phases, malware_types, Related File SDO |
|File | name, hashes |
|Attack Pattern | description, kill_chain_phases, external_references[source_name, external_id, capec] |
|Tool | kill_chain_phases |
|Infrastructure | kill_chain_phases, description |
|Intrusion Set | description |
|Report | description |
|Threat Actor | description |
|Note | author |
|Opinion | author |
|Network Traffic | src_port, dst_port |
|Campaign | description |
|Identity | description |
|Course of Action | description |

| Element | Enforced Requirement |
|:---------|------------:|
|Description | Must be a minimum of 10 words in length |
|UUIDs | Must be of correct type (UUID4 vs UUID5) for each SDO |
|Time | Must be in the expected time format |
|Verbiage | Relationship titles must match the STIX specification |


## Fixer (7 Total)
| Fixer | Description |
|:------|:-----------:|
|SpecVersion |Ensures that Spec Version parameter is present |
|MissingFixer |Create placeholder objects when objects are missing fom relationship objects |
|BrokenRelFixer |Removes relationships that are missing either a Src or Target object |
|UUID5  |Replaces UUIDs from SCOs with UUID5s (Replacement made throughout file) |
|Timestamp  |Ensures proper timestamp formatting |
|Verbiage |Ensures that the correct relationship type is used based on the source and target |

## Holders (11 Total)
| Holder | Description |
|:-----------|----------------------------:| 
|AttackPatternReqHolder | Applies place holder values for missing ‘external_references’, ‘source_name’, ‘capec’ and ‘external_id’ properties in attack-pattern SDOs |
|AuthorReqHolder | Applies place holder values for missing ‘author’ property in various SDOs |
|DescLenHolder | Buffers ‘description’ on various SDOs to meet the minimum length of 10 words |
|DescReqHolder | Applies place holder values for missing ‘description’ property in various SDOs |
|FileReqHolder | Applies place holder values for missing ‘hashes’ property in file SDOs |
|KillChainReqHolder | Applies place holder values for missing ‘kill_chain_phases’ property in various SDOs |
|MalwareReqHolder | Applies place holder values for missing ‘malware_types’ property in malware SDOs |
|NameReqHolder | Applies place holder values for missing ‘name’ property in various SDOs |
|NetworkTrafficReqHolder | Applies place holder values for missing ‘src_port’ and ‘dst_port’ property in network-traffic SDOs |
|SoftwareReqHolder | Applies place holder values for missing ‘cpe’, ‘version’, ‘vendor’ property in software SDOs |
|VulnerabilityReqHolder | Applies place holder values for missing ‘external_references’, ‘source_name’, ‘cve and ‘external_id’ properties in vulnerability SDOs |

## Checkers (12 Total)
| Checker | Description |
|:-----------|----------------------------:| 
|AttackPatternReqChecker | Checks for presence of ‘external_references’, ‘source_name’, ‘capec’ and ‘external_id’ properties in attack-pattern SDOs |
|AuthorReqChecker | Checks for presence of ‘author’ properties in various SDOs |
|DescLenChecker | Checks for SDO descriptions that are less than 10 words in length |
|DescReqChecker | Checks for presence of ‘description’ properties in various SDOs |
|FileReqChecker | Checks for presence of ‘hashes’ properties in various SDOs |
|KillChainReqChecker | Checks for presence of ‘kill_chain_phases’ properties in various SDOs |
|MalwareReqChecker | Checks for presence of ‘malware_types’ properties in malware SDOs |
|AuthorReqChecker | Checks for presence of ‘author’ properties in various SDOs |
|NetworkTrafficReqChecker | Checks for presence of ‘src_port’ and ‘dst_port’ property in network-traffic SDOs |
|SoftwareReqChecker | Checks for presence of ‘cpe’, ‘version’, ‘vendor’ property in software SDOs |
|VulnerabilityReqChecker | Checks for presence of ‘external_references’, ‘source_name’, ‘cve and ‘external_id’ properties in vulnerability SDOs |
|MalwareFileReqChecker | Checks for presence of associated file SDO and relationship objects from malware SDOs |

------------
## Note for Developers:
There is a standard to how new fields to enforce are to be implemented. Any fixer or checker will be put in the appropriate folder. This is because STIX_Enforcer.py uses system calls to go through each folder and run each file. An example of the proper way to ensure a file will run given the system arguments is given below. On another note, output should follow the standard set in place. If an object is changed or flagged, please print the appropriate UUID.
```python
try:
    bundle_input = sys.argv[1]
    bundle_output = sys.argv[2]
    bundleCheck = sys.argv[3]
    
except:
    print('Argument Missing')
    sys.exit()
#Load json files
if bundleCheck == "0":
    with open(bundle_input, 'r') as f:
        bundle = json.load(f)
else:
    with open(bundle_output, 'r') as f:
        bundle = json.load(f)

for object in bundle['objects']:
    #print(object)
    fixed = fixRelationship(object)
    object = fixed

#Save new json bundle
outFile = open(bundle_output, 'w')
outFile.write(json.dumps(bundle))
outFile.close()

print('# Verb Fixer...Done')
```
