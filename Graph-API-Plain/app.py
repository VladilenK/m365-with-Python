import requests
import json
from secrets import clientSc 

clientId = "7e60c372-ec15-4069-a4df-0ab47912da46"
# clientSc = "<imported>" 
tenantId = "7ddc7314-9f01-45d5-b012-71665bb1c544"

apiUri = "https://login.microsoftonline.com/" + tenantId + "/oauth2/v2.0/token"

body = {
    "client_id"     : clientId,
    "client_secret" : clientSc,
    "scope"         : "https://graph.microsoft.com/.default",
    "grant_type"    : "client_credentials" 
}

response = requests.post(apiUri, data=body)
token = json.loads(response.content)["access_token"]

graph_url = 'https://graph.microsoft.com/v1.0/sites/root'
site = requests.get(
    graph_url,
    headers={'Authorization': 'Bearer {0}'.format(token)}
)

print(site.content)
print(json.loads(site.content)["webUrl"])
