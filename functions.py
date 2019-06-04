import os, requests, json

def exportIntegration(baseUrl, id, auth):
    '''Export an integration with a given ID.'''
    url = baseUrl + id + '/archive'
    response = requests.get(url, auth = auth, headers = {'Accept' : 'application/octet-stream'})
    if response.status_code == 200:
        fp = open(id + '.iar','wb')
        fp.write(response.content)
    else:
        response.raise_for_status()

def importIntegration(baseUrl, auth, file):
    '''Import (add or replace) an integration with the same name that was exported previously.'''
    
    url = baseUrl + '/archive'
    files = {'file': open(file, 'rb')}
    
    # Add intgeration
    response = requests.post(url, auth = auth, files = files)
    if response.status_code == 200:
        print('Integration added.')
        exit()

    # Replace integration if it already exists
    if response.status_code == 409:
        files = {'file': open(file, 'rb')}
        response = requests.put(url, auth = auth, files = files)
    
    # Successful operation
    if response.status_code == 204:
        print('Integration replaced.')
        exit()
    
    if response.status_code == 400:
        print('No file is uploaded.')
        response.raise_for_status()
        exit()
    
    if response.status_code == 404:
        print('Integration not found')
        response.raise_for_status()
        exit()
    
    if response.status_code == 500:
        print('Server error.')
        response.raise_for_status()
        exit()
    
def activateIntegration(baseUrl, auth, id):
    '''Activate integration.'''
    url = baseUrl + id
    payload = {'status':'ACTIVATED'}
    changeStatus(url, auth, payload)

def deactivateIntegration(baseUrl, auth, id):
    '''Activate integration.'''
    url = baseUrl + id
    payload = {'status':'CONFIGURED'}
    changeStatus(url, auth, payload)

def changeStatus(url, auth, payload):
    '''Change integration status.'''
    response = requests.post(url, auth = auth, headers = {'Content-Type' : 'application/json', 'X-HTTP-Method-Override' : 'PATCH'}, data = json.dumps(payload))
    if response.status_code == 200:
        print('Status changed.')
        exit()
    else:
        response.raise_for_status()

def retrieveConnections(baseUrl, auth):
    ''' Retrieves a list of connections.'''
    response = requests.get(baseUrl, auth = auth)
    if response.status_code == 200:
        print(response.json())
        exit()
    else:
        response.raise_for_status()