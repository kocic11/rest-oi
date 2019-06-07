import sys, json
import os
import requests
from requests.exceptions import HTTPError
from functions import *

if (len(sys.argv) < 2) :
    print('Usage: parse.py <env.properties>')
    exit()

# Read env.json file
fp = open(sys.argv[1], 'r')
env = json.load(fp)
fp.close()

source = env['source'] + env['integrations']
target = env['target'] + env['integrations']
sourceConnections = env['source'] + env['connections']
targetConnections = env['target'] + env['connections']
headers = {'Accept' : 'application/json'}
auth = (env['user'], env['password'])

# Get all integrations from source
integrations = requests.get(source, auth = auth, headers = headers).json()

# List of all connections used by source integrations
connections = {}

for integration in integrations['items']:
    id = (integration['id']).replace('|', '%7C')
    if integration['status'] == 'ACTIVATED':
        print(id)
        try:
            # exportIntegration(source, id, auth)
            # importIntegration(target, auth, id + '.iar')
            
            
            for conn in integration['endPoints']:
                connId = conn['connection']['id']
                connLink = conn['connection']['links'][0]['href']
                connections[connId] = connLink
            

            # activateIntegration(target, auth, id)
            # deactivateIntegration(source, auth, id)
            # retrieveConnections(sourceConnections, auth)
        except HTTPError as http_err:
            print(f'Http error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

for id in connections:
    # Payload containes connection properties
    payload = {}
    # Group of related properties
    propertiesGroup = []

    for properties in env[id]:
        for property in env[id][properties]:
            keyValue = {}
            keyValue['propertyName'] = property
            keyValue['propertyValue'] = env[id][properties][property]
            if properties == 'attachment':
                try:
                    # Doesn't work for ATP connections:
                    # Bug 29701192 : Upload Connection Property Attachment REST API not working for ATP Connection
                    uploadConnectionPropertyAttachment(targetConnections, auth, id, keyValue['propertyName'], keyValue['propertyValue'])
                except HTTPError as http_err:
                    print(f'Http error occurred: {http_err}')
                    pass
                except Exception as err:
                    print(f'Other error occurred: {err}')
                    pass
            propertiesGroup.append(keyValue)
            payload[properties] = propertiesGroup
            try:
                updateConnection(targetConnections, auth, id, payload)
            except HTTPError as http_err:
                print(f'Http error occurred: {http_err}')
                pass
            except Exception as err:
                print(f'Other error occurred: {err}')
                pass

        # securityProperties = []
        # securityProperty = {}
        # for property in env[id]['securityProperties']:
        #     securityProperty = {}
        #     securityProperty['propertyName'] = property
        #     securityProperty['propertyValue'] = env[id]['securityProperties'][property]
        #     securityProperties.append(securityProperty)
        #     payload['securityProperties'] = securityProperties

        # try:
        #     updateConnection(targetConnections, auth, id, payload)
        #     for property in env[id]['attachment']:
        #         uploadConnectionPropertyAttachment(targetConnections, auth, id, property, env[id]['attachment'][property])
        # except HTTPError as http_err:
        #     print(f'Http error occurred: {http_err}')
        #     pass
        # except Exception as err:
        #     print(f'Other error occurred: {err}')
        #     pass
    # if id == 'ERP_TEST_CONN':
    #     payload = {}
    #     connectionProperties = []
    #     securityProperties = []
    #     for connectionProperty in connection['connectionProperties']:
    #         if connectionProperty['propertyName'] == 'targetWSDLURL':
    #             connectionProperty['propertyValue'] = 'https://ekmt-dev3.fa.us6.oraclecloud.com/fscmService/ServiceCatalogService?WSDL'
    #             connectionProperties.append(connectionProperty)
            
    #     payload['connectionProperties'] = connectionProperties

    #     for securityPolicyInfo in connection['securityPolicyInfo']:
    #         if securityPolicyInfo['securityPolicy'] == 'USERNAME_PASSWORD_TOKEN':
    #             payload['securityPolicy'] = 'USERNAME_PASSWORD_TOKEN'
    #             for securityProperty in securityPolicyInfo['securityProperties']:
    #                 if securityProperty['propertyName'] == 'username':
    #                     securityProperty['propertyValue'] = 'integrationuser'
    #                     securityProperties.append(securityProperty)
    #                 if securityProperty['propertyName'] == 'password':
    #                     securityProperty['propertyValue'] = 'Welcome1'
    #                     securityProperties.append(securityProperty)
                        
    #     payload['securityProperties'] = securityProperties
    #     updateConnection(targetConnections, auth, id, payload)

    # if id == 'ATP_PERF_COMMON':
    #     payload = {}
    #     connectionProperties = []
    #     securityProperties = []
    #     for connectionProperty in connection['connectionProperties']:
    #         if connectionProperty['propertyName'] == 'ServiceName':
    #             connectionProperty['propertyValue'] = 'atpstage_low'
    #             connectionProperties.append(connectionProperty)
            
    #     payload['connectionProperties'] = connectionProperties

    #     for securityPolicyInfo in connection['securityPolicyInfo']:
    #         if securityPolicyInfo['securityPolicy'] == 'JDBC_OVER_SSL':
    #             payload['securityPolicy'] = 'JDBC_OVER_SSL'
    #             for securityProperty in securityPolicyInfo['securityProperties']:
    #                 if securityProperty['propertyName'] == 'WALLETPASSWORD':
    #                     securityProperty['propertyValue'] = 'm&7RCzZcK6jLXh'
    #                     securityProperties.append(securityProperty)
    #                 if securityProperty['propertyName'] == 'UserName':
    #                     securityProperty['propertyValue'] = 'airbnb_common'
    #                     securityProperties.append(securityProperty)
    #                 if securityProperty['propertyName'] == 'Password':
    #                     securityProperty['propertyValue'] = 'D55k8qze4Bx3LT49'
    #                     securityProperties.append(securityProperty)
                        
    #     payload['securityProperties'] = securityProperties
    #     updateConnection(targetConnections, auth, id, payload)
    #     uploadConnectionPropertyAttachment(targetConnections, auth, id, 'WALLET', 'ATPSTAGE.zip')


