import sys, json, os, requests
from requests.exceptions import HTTPError
from functions import *

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
integrations = getIntegrations(sourceUrl, sourceAuth, headers, 'ACTIVATED')

# Export integrations 
#exportIntegrations(integrations, sourceUrl, sourceAuth)

# Import integrations
#importIntegrations(integrations, targetUrl, targetAuth)

# COnfigure connections
updateConnections(integrations, env, targetConnectionsUrl, targetAuth)

# Deactivate integrations
deactivateIntegrations(integrations, sourceUrl, sourceAuth)

# Activate integrations and enable tracing
activateIntegrations(integrations, sourceUrl, sourceAuth, 'true')