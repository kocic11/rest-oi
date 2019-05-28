#!/bin/bash

source ./env.properties
# Retrieve Integrations
curl --silent -u $user:$password -o integrations.json \
 -H "Accept: application/json" \
 -X GET \
 $server/ic/api/integration/v1/integrations

# Retrieve Integration
curl --silent -u $user:$password -o $id.json \
 -H "Accept: application/json" \
 -X GET \
 $server/ic/api/integration/v1/integrations/$id 

 # Export an Integration
curl --silent -u $user:$password -o $id.iar \
 -X GET \
 -H "Accept: application/octet-stream" \
 $server/ic/api/integration/v1/integrations/$id/archive

 # Retrieve and process Integrations
curl --silent -u $user:$password -o ./integrations.json \
 -H "Accept: application/json" \
 -X GET \
 $server/ic/api/integration/v1/integrations?orderBy=id | python3 parse.py ./integrations.json


