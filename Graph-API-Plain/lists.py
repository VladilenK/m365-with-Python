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

# Get root site
graph_url = 'https://graph.microsoft.com/v1.0/sites/root'
site = requests.get(   graph_url,    headers={'Authorization': 'Bearer {0}'.format(token)})
print("================================================================================================")
print("Root site: ")
print(json.loads(site.content)["webUrl"])
print("\n")

# Get specific site by site rel path
site_id = "s5dz3.sharepoint.com:/sites/tst"
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '?$select=id,webUrl,displayName'
site = requests.get(
    graph_url,
    headers={'Authorization': 'Bearer {0}'.format(token)}
)
print("Specific site: ")
print("webUrl: ", json.loads(site.content)["webUrl"])
print("id: ", json.loads(site.content)["id"])
print("displayName: ", json.loads(site.content)["displayName"])
print("\n")

# Get site lists
site_id = "d659b49c-9e0d-4cc4-95bb-4cc377a2d8ba"
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/lists'
lists = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
print("Site lists:")
for list in json.loads(lists.content)["value"]:
    print("  Display Name:", list["displayName"])
    print("   Id:", list["id"])
    print("   Web Url:", list["webUrl"])
    print("   Created Date:", list["createdDateTime"])
    print("   Last Modified Date:", list["lastModifiedDateTime"])
    
print("\n")

# Get specific site list
site_id = "d659b49c-9e0d-4cc4-95bb-4cc377a2d8ba"
list_id = "0da06cea-7df7-4bab-8273-e3e5191c9bfb"
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/lists/' + list_id
list = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
print("Specific site list:")
print("  Display name: ", json.loads(list.content)["displayName"])
print("\n")

# get list items
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/lists/' + list_id + '/items'
list_items = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
print("List items:")
for item in json.loads(list_items.content)["value"]:
    print(" ", item["id"], item["createdDateTime"] ,item["webUrl"], item["contentType"]["name"])
    
print("\n")

# get list items with columns
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/lists/' + list_id + '/items?$expand=fields'
list_items = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
print("List items Columns:")
# print(list_items.content)
# print(json.loads(list_items.content))
for item in json.loads(list_items.content)["value"]:
    print(" ", item["id"], item["createdDateTime"] ,item["webUrl"], item["contentType"]["name"])
    print(" ", item["fields"]["FileSizeDisplay"], item["fields"]["FileLeafRef"])

print("\n")

# get specific list item with columns
item_id = "2"
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/lists/' + list_id + '/items/' + item_id + '?$expand=fields'
list_item = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
print("List item:")
item = json.loads(list_item.content)
print("  Title:", item["fields"]["Title"])
print("  Custom field:", item["fields"]["CustomField1"])

print("\n")

