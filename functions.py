import os, requests, json

def exportIntegration(baseUrl, id, auth):
    '''Export an integration with a given ID.'''
    url = baseUrl + '/' + id + '/archive'
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
        return

    # Replace integration if it already exists
    if response.status_code == 409:
        files = {'file': open(file, 'rb')}
        response = requests.put(url, auth = auth, files = files)
        # Successful operation
        if response.status_code == 204:
            print('Integration replaced.')
            return
    
    if response.status_code == 400:
        print('No file is uploaded.')
        response.raise_for_status()
    
    if response.status_code == 404:
        print('Integration not found')
        response.raise_for_status()
    
    if response.status_code == 500:
        print('Server error.')
        response.raise_for_status()
    
def activateIntegration(baseUrl, auth, id, tracing):
    '''Activate integration and enable tracing.'''
    url = baseUrl + '/' + id
    payload = {'status':'ACTIVATED', 'payloadTracingEnabledFlag': tracing}
    changeStatus(url, auth, payload)

def deactivateIntegration(baseUrl, auth, id):
    '''Deactivate integration.'''
    url = baseUrl + '/' + id
    payload = {'status':'CONFIGURED'}
    changeStatus(url, auth, payload)

def changeStatus(url, auth, payload):
    '''Change integration status.'''
    response = requests.post(url, auth = auth, headers = {'Content-Type' : 'application/json', 'X-HTTP-Method-Override' : 'PATCH'}, data = json.dumps(payload))
    if response.status_code == 200:
        print(f'Status changed to {payload["status"]}')
        return
    if response.status_code == 412:
        print("Already activated/deactivated or can't be activated/deactivated")
        return
        
    response.raise_for_status()

def retrieveConnections(baseUrl, auth):
    ''' Retrieve a list of connections.'''
    response = requests.get(baseUrl, auth = auth)
    if response.status_code == 200:
        connections = response.json()
    else:
        response.raise_for_status()

def retrieveConnection(url, auth):
    ''' Retrieve a connection.'''
    response = requests.get(url, auth = auth, headers = {'Accept' : 'application/json'})
    if response.status_code == 200:
        return response.json()
    
    response.raise_for_status()

def updateConnection(url, auth, name, payload):
    ''' Update a connection.'''
    url = url + '/' + name
    response = requests.post(url, auth = auth, headers = {'X-HTTP-Method-Override' : 'PATCH', 'Content-Type' : 'application/json'}, data = json.dumps(payload))
    if response.status_code in [200, 400]:
        return
    
    response.raise_for_status()

def uploadConnectionPropertyAttachment(url, auth, id, connPropName, file):
    ''' Upload a connection property attachment.'''
    url = url + '/' + id + '/attachments/' + connPropName
    files = {'file': open(file, 'rb')}
    response = requests.post(url, auth = auth, files = files)
    if response.status_code in [200, 400]:
        return
    
    response.raise_for_status()

def getIntegrations(url, auth, headers, status):
    '''Get integrations based on status.'''
    try:
        response = requests.get(url, auth = auth, headers = headers).json()       
        integrations = {}
        for integration in response['items']:
            if integration['status'] == status:
                id = (integration['id']).replace('|', '%7C')
                integrations[id] = integration
        return  integrations
    except HTTPError as http_err:
        print(f'Http error occurred: {http_err}')
        exit
    except Exception as err:
        print(f'Other error occurred: {err}')
        exit

def updateConnections(integrations, env, connectionsUrl, auth):
    '''Configure the connections used by source integrations at target'''
    # Get integration connections and add them to the list of connections
    connections = {}
    for id in integrations:
        for connection in integrations[id]['endPoints']:
            connId = connection['connection']['id']
            link = connection['connection']['links'][0]['href']
            connections[connId] = link

    for id in connections:
        # Payload containes connection properties
        payload = {}
        # Attachment properties
        attachment = {}
        if id in env:
            for group in env[id]:
                # Group of properties name
                properties = env[id][group]
                if group != 'attachment':
                    propertiesGroup = []
                    for propertyName in properties:
                        property = {}
                        property['propertyName'] = propertyName
                        property['propertyValue'] = properties[propertyName]
                        propertiesGroup.append(property)
                    payload[group] = propertiesGroup
                else:
                    for propertyName in properties:
                        attachment = {}
                        attachment['propertyName'] = propertyName
                        attachment['propertyValue'] = properties[propertyName]
                        
            print(f'Updating connection {id}: {payload}')
            try:
                updateConnection(connectionsUrl, auth, id, payload)
                # Doesn't work for ATP connections:
                # Bug 29701192 : Upload Connection Property Attachment REST API not working for ATP Connection
                uploadConnectionPropertyAttachment(connectionsUrl, auth, id, attachment['propertyName'], attachment['propertyValue'])
            except HTTPError as http_err:
                print(f'Http error occurred: {http_err}')
                pass
            except Exception as err:
                print(f'Other error occurred: {err}')
                pass

def exportIntegrations(integrations, url, auth):
    '''Export integrations'''
    for id in integrations:
        print(f'Export integration: {id}')
        try:
            # Export integration
            exportIntegration(url, id, auth)
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass

def importIntegrations(integrations, url, auth):
    '''Import integrations'''
    for id in integrations:
        print(f'Import integration: {id}')
        try:
            importIntegration(url, auth, id + '.iar')
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass

def activateIntegrations(integrations, url, auth, tracing):
    '''Activate integrations.'''
    for id in integrations:
        print(f'Activate integration {id}')
        try:
            activateIntegration(url, auth, id, tracing)
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass

def deactivateIntegrations(integrations, url, auth):
    ''' Deactivate integrations.'''
    for id in integrations:
        print(f'Deactivate integration {id}')
        try:
            deactivateIntegration(url, auth, id)
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass