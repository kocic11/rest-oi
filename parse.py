import json
import os
import sys

import requests
from requests.exceptions import HTTPError

from functions import getIntegrations, getLookups, getConnection, getConnections, exportIntegrations, exportLookups

# Begin
lenArgs = len(sys.argv)
if (lenArgs < 2) :
    print('Usage: parse.py <env.json>')
    exit()

# Read env.json file
fp = open(sys.argv[1], 'r')
env = json.load(fp)
fp.close()

sourceIntegrations = env['sourceUrl'] + env['integrations']
targetIntegrations = env['targetUrl'] + env['integrations']
sourceConnections = env['sourceUrl'] + env['connections']
targetConnections = env['targetUrl'] + env['connections']
sourceLookups = env['sourceUrl'] + env['lookups']
targetLookups = env['targetUrl'] + env['lookups']
headers = {'Accept' : 'application/json'}
sourceAuth = (env['sourceUser'], env['sourcePassword'])
targetAuth = (env['targetUser'], env['targetPassword'])

# Get active configurations
integrations = getIntegrations(sourceIntegrations, sourceAuth, headers, 'ACTIVATED')

# Write integrations JSON file
fp = open('integrations.json','w')
fp.write(json.dumps(integrations, indent=4))
fp.close()

lookups = getLookups(sourceLookups, sourceAuth)
fp = open('lookups.json','w')
fp.write(json.dumps(lookups, indent=4))
fp.close()

connections = getConnections(integrations, sourceConnections, sourceAuth)
fp = open('connections.json','w')
fp.write(json.dumps(connections, indent=4))
fp.close()

connection = getConnection(connections['ODI_FILE_PICKUP'], sourceAuth)
fp = open('ODI_FILE_PICKUP.json','w')
fp.write(json.dumps(connection, indent=4))
fp.close()

# exportIntegration(sourceIntegrations, sourceAuth, 'SCHEDULE_FBDI%7C03.20.0000')
# deactivateIntegration(targetIntegrations, targetAuth, 'SCHEDULE_FBDI%7C03.10.0000')
# importIntegration(targetIntegrations, targetAuth, 'SCHEDULE_FBDI%7C03.20.0000.iar')
# activateIntegration(targetIntegrations, targetAuth, 'SCHEDULE_FBDI%7C03.20.0000', 'true')

# Export integrations 
exportIntegrations(integrations, sourceIntegrations, sourceAuth)

# Export lookups 
exportLookups(lookups, sourceLookups, sourceAuth)

# Import lookups 
# importLookups(lookups, targLookups, targetAuthAuth)

# Configure connections
# updateConnections(connections, env, targetConnections, targetAuth)

# # Pause integrations
# pauseSchedule(sourceIntegrations, sourceAuth, 'SCHEDULE_PAAS_METADATA_REFRESH%7C01.80.0000')
# pauseSchedule(sourceIntegrations, sourceAuth, 'EXCHANGE_RATES_OLD%7C02.00.0000')

# # Deactivate integrations
# deactivateIntegrations(integrations, targetIntegrations, targetAuth)

# Import integrations
# importIntegrations(integrations, targetIntegrations, targetAuth)

# Activate integrations and enable tracing
# activateIntegrations(integrations, targetIntegrations, targetAuth, 'true')

# # Resume integrations
# resumeSchedule(sourceIntegrations, sourceAuth, 'SCHEDULE_PAAS_METADATA_REFRESH%7C01.80.0000')
# resumeSchedule(sourceIntegrations, sourceAuth, 'EXCHANGE_RATES_OLD%7C02.00.0000')
