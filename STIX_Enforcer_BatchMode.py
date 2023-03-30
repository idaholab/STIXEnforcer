#Copyright 2023, Battelle Energy Alliance, LLC

import os, sys, glob

'''
try:
    folder = sys.argv[1]
except:
    print('Missing Argument')
    exit()
'''

path = ""
while not os.path.isdir(path):
    path = input("Full Path to Directory of JSON Bundles: ")

jsonInput = []  
  
#Collect List of Files
for entry in os.listdir(path):
    jsonInput.append(path + os.sep + entry)

#print(jsonInput)

for jsonFile in jsonInput:
    print()
    print('############################################################')
    print('STIXEnforcing: ' +  jsonFile)
    os.system(sys.executable + ' STIX_Enforcer.py ' + jsonFile + ' ' + jsonFile.split('.json')[0] + '_Enforced2.json')
    print('############################################################')
