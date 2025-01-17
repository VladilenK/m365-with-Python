import requests
import json
from secrets import clientSc, clientId, tenantId, siteId, listId 

# specify client id, client secret and tenant id
# clientId = ""
# clientSc = "" 
# tenantId = "" 

apiUri = "https://login.microsoftonline.com/" + tenantId + "/oauth2/v2.0/token"

body = {
    "client_id"     : clientId,
    "client_secret" : clientSc,
    "scope"         : "https://graph.microsoft.com/.default",
    "grant_type"    : "client_credentials" 
}

try: 
    response = requests.post(apiUri, data=body)
    token = json.loads(response.content)["access_token"]
except:
    print("Error: ", json.loads(response.content)["error_description"])
    exit()

print("Got token: ", token[0:10], "...")
headers={'Authorization': 'Bearer {0}'.format(token)}

# Get root site
print("Geting root site")
graph_url = 'https://graph.microsoft.com/v1.0/sites/root'
graphResponse = requests.get(   graph_url, headers=headers )
print(" Response status code: ", graphResponse.status_code)

# Get specific site by site rel path
print("Geting specific site")
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + siteId + '?$select=id,webUrl,displayName'
graphResponse = requests.get(   graph_url, headers=headers )
print(" Response status code: ", graphResponse.status_code)
if graphResponse.status_code == 200:
    site = json.loads(graphResponse.content)
    print(" Site display name: ", site["displayName"])

# Get site lists
print("Geting site lists")
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + siteId + '/lists'
graphResponse = requests.get(   graph_url, headers=headers )
print(" Response status code: ", graphResponse.status_code)
if graphResponse.status_code == 200:
    lists = json.loads(graphResponse.content)["value"]
    for list in lists:
        print("  Site list: ", list["name"])

# Get specific site list
print("Geting specific site list")
# graph_url = 'https://graph.microsoft.com/v1.0/sites/' + siteId + '/lists/' + listId
graph_url = 'https://graph.microsoft.com/beta/sites/' + siteId + '/lists/' + listId
graphResponse = requests.get(   graph_url, headers=headers )
print(" Response status code: ", graphResponse.status_code)
if graphResponse.status_code == 200:
    list = json.loads(graphResponse.content)
    print(" List display name: ", list["displayName"])

# get list items
print("Geting list items")
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + siteId + '/lists/' + listId + '/items'
graphResponse = requests.get(   graph_url, headers=headers )
print(" Response status code: ", graphResponse.status_code)
if graphResponse.status_code == 200:
    listItems = json.loads(graphResponse.content)["value"]
    for item in listItems:
        print("  List item: ", item["webUrl"].split("/")[-1])

