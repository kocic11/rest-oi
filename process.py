import json
import os
import sys

import requests
from requests.exceptions import HTTPError

from functions import __updateSchedule, getIntegrations, getLookups, getConnections, exportIntegrations, updateConnections, deactivateIntegrations, importIntegrations, activateIntegrations, __exportIntegration, __importIntegration, __pauseSchedule, __resumeSchedule

# Begin
lenArgs = len(sys.argv)
if (lenArgs < 2) :
    print('Usage: process.py <env.json>')
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
integrations = getIntegrations(targetIntegrations, targetAuth, headers, 'ACTIVATED')

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

fp = open('schedule.json','r')
payload = json.load(fp)
fp.close()

# __updateSchedule(sourceIntegrations, sourceAuth, 'EXCHANGE_RATES_OLD%7C02.00.0000', payload)

# connection = getConnection(connections['ODI_FILE_PICKUP'], sourceAuth)
# fp = open('ODI_FILE_PICKUP.json','w')
# fp.write(json.dumps(connection, indent=4))
# fp.close()

# __exportIntegration(sourceIntegrations, sourceAuth, 'SCHEDULE_PAAS_METADATA_REFRESH%7C02.00.0000')
# deactivateIntegration(targetIntegrations, targetAuth, 'SCHEDULE_FBDI%7C03.10.0000')
# __importIntegration(sourceIntegrations, sourceAuth, 'SCHEDULE_PAAS_METADATA_REFRESH%7C02.00.0000.iar')
# activateIntegration(targetIntegrations, targetAuth, 'SCHEDULE_FBDI%7C03.20.0000', 'true')

# Export integrations 
exportIntegrations(integrations, sourceIntegrations, sourceAuth)

# Export lookups 
# exportLookups(lookups, sourceLookups, sourceAuth)

# Import lookups 
# importLookups(lookups, targLookups, targetAuthAuth)

# Configure connections
updateConnections(connections, targetIntegrations, targetAuth, env)

# Pause integrations
__pauseSchedule(targetIntegrations, targetAuth, 'SCHEDULE_PAAS_METADATA_REFRESH%7C01.80.0000')
__pauseSchedule(targetIntegrations, targetAuth, 'EXCHANGE_RATES_OLD%7C02.00.0000')

# Deactivate integrations
deactivateIntegrations(integrations, targetIntegrations, targetAuth)

# Import integrations
importIntegrations(integrations, targetIntegrations, targetAuth)

# Activate integrations and enable tracing
activateIntegrations(integrations, targetIntegrations, targetAuth, 'true')

# # Resume integrations
__resumeSchedule(targetIntegrations, targetAuth, 'SCHEDULE_PAAS_METADATA_REFRESH%7C01.80.0000')
__resumeSchedule(targetIntegrations, targetAuth, 'EXCHANGE_RATES_OLD%7C02.00.0000')
