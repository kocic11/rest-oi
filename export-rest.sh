#!/bin/bash

source ./env.properties
# Retrieve Integrations
curl --silent -u $user:$password -o integrations.json \
 -H "Accept: application/json" \
 -X GET \
 $server/ic/api/integration/v1/integrations

curl -v -u $user:$password -F "file"="@./EH_TEST%7C01.00.0000.iar" \
 -H "Accept: application/json" \
 -X PUT \
 $server/ic/api/integration/v1/integrations/archive

# Deactivate integration
curl -v -u $user:$password \
 -H "Content-Type:application/json" \
 -H "X-HTTP-Method-Override:PATCH" \
 -d @configured.json \
 -X POST \
 $server/ic/api/integration/v1/integrations/EH_TEST%7C01.00.0000

# Activate configuration
curl -v -u $user:$password \
 -H "Content-Type:application/json" \
 -H "X-HTTP-Method-Override:PATCH" \
 -d @activated.json \
 -X POST \
 $server/ic/api/integration/v1/integrations/EH_TEST%7C01.00.0000

# # Retrieve Integration
# curl --silent -u $user:$password -o $id.json \
#  -H "Accept: application/json" \
#  -X GET \
#  $server/ic/api/integration/v1/integrations/$id 

#  # Export an Integration
# curl --silent -u $user:$password -o $id.iar \
#  -X GET \
#  -H "Accept: application/octet-stream" \
#  $server/ic/api/integration/v1/integrations/$id/archive

#  # Retrieve and process Integrations
#  # q={name like 'org'} & {status like 'all'}
#  #  
#  # q=%7Bname%20like%20%27org%27%7D%20%26%20%7Bstatus%20like%20%27all%27%7D
# curl --silent -u $user:$password -o ./integrations.json \
#  -H "Accept: application/json" \
#  -X GET \
#  $server/ic/api/integration/v1/integrations?q%3D%7Bstatus%3A%27ACTIVATED%27%7D
 
# python3 parse.py ./integrations.json ./env.json


