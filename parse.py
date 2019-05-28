import sys, json;
import os
if (len(sys.argv) < 2) :
    print("Usage: parse.py <file.json>.")
    exit()
    
fp = open(sys.argv[1], "r")
obj = json.load(fp)
fp.close()
print("\n")
print("totalResults: " + str(obj['totalResults']) + "\n")
for num in range (0, obj['totalResults']):
    print(str(num) + ": " + obj['items'][num]['id'])