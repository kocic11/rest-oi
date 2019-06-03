import sys, json
import os
import requests
from functions import exportIntegration, importIntegration

if (len(sys.argv) < 2) :
    print('Usage: parse.py <env.properties>')
    exit()

# Read env.json file
fp = open(sys.argv[1], 'r')
env = json.load(fp)
fp.close()

baseUrl = env['server'] + '/ic/api/integration/v1/integrations/'
headers = {'Accept' : 'application/json'}
auth = (env['user'], env['password'])

ints = requests.get(baseUrl, auth = auth, headers = headers).json()

print('\n')
print('totalResults: ' + str(ints['totalResults']) + '\n')
for num in range (0, ints['totalResults']):
    id = (ints['items'][num]['id']).replace('|', '%7C')
    url = baseUrl + id
    response = requests.get(url, auth = auth, headers = headers)
    if response.json()['status'] == 'ACTIVATED':
        print(str(num) + ': ' + id)
        exportIntegration(baseUrl, id, auth)


