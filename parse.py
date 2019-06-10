import sys, json, os, requests
from requests.exceptions import HTTPError
from functions import *

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

def configureConnections(integrations, env, connectionsUrl, auth):
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

# Begin
lenArgs = len(sys.argv)
if (lenArgs < 2) :
    print('Usage: parse.py <env.properties>')
    exit()

# Read env.json file
fp = open(sys.argv[1], 'r')
env = json.load(fp)
fp.close()

sourceUrl = env['sourceUrl'] + env['integrations']
targetUrl = env['targetUrl'] + env['integrations']
sourceConnections = env['sourceUrl'] + env['connections']
targetConnectionsUrl = env['targetUrl'] + env['connections']
headers = {'Accept' : 'application/json'}
sourceAuth = (env['sourceUser'], env['sourcePassword'])
targetAuth = (env['targetUser'], env['targetPassword'])

# Get active configurations
activeIntegrations = getIntegrations(sourceUrl, sourceAuth, headers, 'ACTIVATED')

# Export integrations 
#exportIntegrations(activeIntegrations, sourceUrl, sourceAuth)

# Import integrations
#importIntegrations(activeIntegrations, targetUrl, targetAuth)

# COnfigure connections
configureConnections(activeIntegrations, env, targetConnectionsUrl, targetAuth)

# Deactivate integrations
deactivateIntegrations(activeIntegrations, sourceUrl, sourceAuth)

# Activate integrations and enable tracing
activateIntegrations(activeIntegrations, sourceUrl, sourceAuth, 'true')