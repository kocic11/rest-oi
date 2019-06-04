import sys, json
import os
import requests
from requests.exceptions import HTTPError
from functions import exportIntegration, importIntegration, activateIntegration, deactivateIntegration, retrieveConnections

if (len(sys.argv) < 2) :
    print('Usage: parse.py <env.properties>')
    exit()

# Read env.json file
fp = open(sys.argv[1], 'r')
env = json.load(fp)
fp.close()

baseUrlInt = env['server'] + '/ic/api/integration/v1/integrations'
baseUrlConn = env['server'] + '/ic/api/integration/v1/connections'
headers = {'Accept' : 'application/json'}
auth = (env['user'], env['password'])

ints = requests.get(baseUrlInt, auth = auth, headers = headers).json()

print('\n')
print('totalResults: ' + str(ints['totalResults']) + '\n')
# for num in range (0, ints['totalResults']):
#     id = (ints['items'][num]['id']).replace('|', '%7C')
#     url = baseUrlInt + id
#     response = requests.get(url, auth = auth, headers = headers)
#     # if response.json()['status'] == 'ACTIVATED':
#     print(str(num) + ': ' + id)
#     exportIntegration(baseUrlInt, id, auth)
try:
    # importIntegration(baseUrlInt, auth, './EH_TEST%7C01.00.0000.iar')
    # activateIntegration(baseUrlInt, auth, '/EH_TEST%7C01.00.0000')
    # deactivateIntegration(baseUrlInt, auth, '/EH_TEST%7C01.00.0000')
    retrieveConnections(baseUrlConn, auth)
except HTTPError as http_err:
    print(f'Http error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    print('Success!')


