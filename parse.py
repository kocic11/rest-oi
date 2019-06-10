import sys, json, os, requests
from requests.exceptions import HTTPError
from functions import *

def getActiveIntegrations(url, auth, headers):
    '''Get all active integrations from source.'''
    try:
        integrations = requests.get(sourceUrl, auth = sourceAuth, headers = headers).json()       
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

def configureConnections(integrations, env, targetConnectionsUrl, targetAuth):
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
                updateConnection(targetConnectionsUrl, targetAuth, id, payload)
                # Doesn't work for ATP connections:
                # Bug 29701192 : Upload Connection Property Attachment REST API not working for ATP Connection
                uploadConnectionPropertyAttachment(targetConnectionsUrl, targetAuth, id, attachment['propertyName'], attachment['propertyValue'])
            except HTTPError as http_err:
                print(f'Http error occurred: {http_err}')
                pass
            except Exception as err:
                print(f'Other error occurred: {err}')
                pass

def exportImportIntegrations(integrations, sourceUrl, targetUrl, sourceAuth, targetAuth):
    '''Export integrations from source and import them to target'''
    for integration in integrations:
        id = integrations['id']
        # # Only export/import active integrations
        # if integration['status'] == 'ACTIVATED':
        print(f'Export/Import integration: {id}')
        # activeIntegrations.append(id)
        try:
            # Export integration from source
            exportIntegration(sourceUrl, id, sourceAuth)
            
            # Import integration to target
            importIntegration(targetUrl, targetAuth, id + '.iar')

            # # Get integration connections and add them to the list of connections
            # for conn in integration['endPoints']:
            #     connId = conn['connection']['id']
            #     connLink = conn['connection']['links'][0]['href']
            #     connections[connId] = connLink
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass

def rectivateIntegrations(integrations, targetUrl, targetAuth):
    ''' Reactivate imported integrations.'''
    for id in integrations:
        print(f'Reactivate integration {id}')
        try:
            deactivateIntegration(targetUrl, targetAuth, id)
            activateIntegration(targetUrl, targetAuth, id, 'true')
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
            pass
        except Exception as err:
            print(f'Other error occurred: {err}')
            pass

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

activeIntegrations = getActiveIntegrations(sourceUrl, sourceAuth, headers)
# exportImportIntegrations(activeIntegrations, sourceUrl, targetUrl, sourceAuth, targetAuth)
# configureConnections(activeIntegrations, env, targetConnectionsUrl, targetAuth)
# rectivateIntegrations(activeIntegrations, targetUrl, targetAuth)
rectivateIntegrations(activeIntegrations, sourceUrl, targetAuth)