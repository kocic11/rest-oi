import os, requests

def exportIntegration(baseUrl, id, auth):
    """Export an integration with a given ID."""
    url = baseUrl + id + '/archive'
    response = requests.get(url, auth = auth, headers = {'Accept' : 'application/octet-stream'})
    if response.status_code == 200:
        fp = open(id + '.iar','w+b')
        fp.write(response.content)

def importIntegration(baseUrl, id, auth):
    """Import an integration with a given ID."""
    url = baseUrl + id + '/archive'
    response = requests.post(url, auth = auth, headers = {'Accept' : 'application/octet-stream'})
    if response.status_code == 200:
        fp = open(id + '.iar','w+b')
        fp.write(response.content)
