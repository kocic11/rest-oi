import sys, json;
import os
import requests

if (len(sys.argv) < 3) :
    print('Usage: parse.py <file.json> <env.properties>')
    exit()

# Read integrations.json file
fp = open(sys.argv[1], 'r')
ints = json.load(fp)

# Read env.json file
fp = open(sys.argv[2], 'r')
env = json.load(fp)
fp.close()

baseUrl = env['server'] + '/ic/api/integration/v1/integrations/'
headers = {'Accept' : 'application/json'}
auth = (env['user'], env['password'])
print('\n')
print('totalResults: ' + str(ints['totalResults']) + '\n')
for num in range (0, ints['totalResults']):
    id = (ints['items'][num]['id']).replace('|', '%7C')
    url = baseUrl + id
    response = requests.get(url, auth = auth, headers = headers)
    if response.json()['status'] == 'ACTIVATED':
        print(str(num) + ': ' + id)
        url = url + '/archive'
        response = requests.get(url, auth = auth, headers = {'Accept' : 'application/octet-stream'})
        if response.status_code == 200:
            fp = open(id + '.iar','w+b')
            fp.write(response.content)



