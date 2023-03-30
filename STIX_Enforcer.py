#Copyright 2023, Battelle Energy Alliance, LLC

import os, sys, glob

#Collect List of Scripts
checkers = glob.glob("Checkers/*.py")
fixers = glob.glob("Fixers/*.py")
holders = glob.glob("Holders/*.py")

try:
    bundle = sys.argv[1]
except:
    print('Missing Argument')
    exit()
try:
    output = sys.argv[2]
except:
    output = bundle

bundleCheck = 0 # provides the logic for which file is called first so it can fill in the empty file supplied in arg2

print('STIX Enforcer - Holders')
print('------------------------')
sys.stdout.flush()
for holder in holders:
    os.system(sys.executable + ' .'  + os.sep + holder + ' ' + bundle + ' ' + output + ' ' + str(bundleCheck))
    bundleCheck += 1 #Marks the first file as having been run 
    print()

print()
print('STIX Enforcer - Fixers')
print('------------------------')
sys.stdout.flush()
for fixer in fixers:
    os.system(sys.executable + ' .'  + os.sep + fixer + ' ' + bundle + ' ' + output + ' ' + str(bundleCheck))
    bundleCheck += 1 #Marks the first file as having been run 
    print()

print()
print('STIX Enforcer - Checkers')
print('------------------------')
sys.stdout.flush()
for checker in checkers:
    if bundleCheck == 0:
        os.system(sys.executable + ' .'  + os.sep + checker + ' ' + bundle)
        bundleCheck += 1
    else:
        os.system(sys.executable + ' .'  + os.sep + checker + ' ' + output)
    print()    
