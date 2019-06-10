import sys, json, os, requests
from requests.exceptions import HTTPError
from functions import *

def getActiveIntegrations(url, auth, headers):
    '''Get all active integrations from source.'''
    try:
        integrations = requests.get(url, auth = auth, headers = headers).json()       
        activeIntegrations = {}
        for integration in integrations['items']:
            id = (integration['id']).replace('|', '%7C')
            if integration['status'] == 'ACTIVATED':
                print(f'Export/Import integration: {id}')
                activeIntegrations[id] = integration
        return  activeIntegrations
    except HTTPError as http_err:
        print(f'Http error occurred: {http_err}')
        exit
    except Exception as err:
        print(f'Other error occurred: {err}')
        exit

def configureConnections(integrations, env, connectionsUrl, auth):
    '''Configure the connections used by source integrations at target'''
    # Get integration connections and add them to the list of connections
    connections = []
    for integration in integrations:
        for conn in integration['endPoints']:
            id = conn['connection']['id']
            link = conn['connection']['links'][0]['href']
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
                # Group of related properties
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
    '''Export integrations from source and import them to target'''
    for integration in integrations:
        id = integrations['id']
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
    '''Export integrations from source and import them to target'''
    for integration in integrations:
        id = integrations['id']
        print(f'Export/Import integration: {id}')
        try:
            # Import integration to target
            importIntegration(url, auth, id + '.iar')
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass


def activateIntegrations(integrations, url, auth, tracing):
    ''' Activate integrations.'''
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
activeIntegrations = getActiveIntegrations(sourceUrl, sourceAuth, headers)

# Export integrations 
exportIntegrations(activeIntegrations, sourceUrl, sourceAuth)

# Import integrations
importIntegrations(activeIntegrations, targetUrl, targetAuth)

# COnfigure connections
configureConnections(activeIntegrations, env, targetConnectionsUrl, targetAuth)

# Deactivate integrations
deactivateIntegrations(activeIntegrations, sourceUrl, sourceAuth)

# Activate integrations and enable tracing
activateIntegrations(activeIntegrations, sourceUrl, sourceAuth, 'true')