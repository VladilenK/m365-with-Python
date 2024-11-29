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

# Get site drives
site_id = "d659b49c-9e0d-4cc4-95bb-4cc377a2d8ba"
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/drives'
drives = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
print("Site libraries (drives):")
for drive in json.loads(drives.content)["value"]:
    # print("  Drive")
    # print(drive)
    print("  Name:", drive["name"])
    print("   Id:", drive["id"])
    print("   Drive Type:", drive["driveType"])
    print("   Web Url:", drive["webUrl"])
    print("   Created Date:", drive["createdDateTime"])
    print("   Last Modified Date:", drive["lastModifiedDateTime"])
    
print("\n")

# Get site's default drives
site_id = "d659b49c-9e0d-4cc4-95bb-4cc377a2d8ba"
graph_url = 'https://graph.microsoft.com/v1.0/sites/' + site_id + '/drive'
drive = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
drive = json.loads(drive.content)
print("Site's default document library (drive):")
print("  Name:", drive["name"])
print("   Id:", drive["id"])
print("   Drive Type:", drive["driveType"])
print("   Web Url:", drive["webUrl"])
print("   Created Date:", drive["createdDateTime"])
print("   Last Modified Date:", drive["lastModifiedDateTime"])
print("\n")

# Get specific drive
# site_id = "d659b49c-9e0d-4cc4-95bb-4cc377a2d8ba"
drive_id = "b!nLRZ1g2exEyVu0zDd6LYuqbIIh75Y7ZKhoLRLGvwXzVXewcZecd-R6CP5rCPiYSu"
graph_url = 'https://graph.microsoft.com/v1.0/drives/' + drive_id
drive = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
drive = json.loads(drive.content)
print("Specific document library (drive) by Drive Id:")
print("  Name:", drive["name"])
print("   Id:", drive["id"])
print("   Drive Type:", drive["driveType"])
print("   Web Url:", drive["webUrl"])
print("   Created Date:", drive["createdDateTime"])
print("   Last Modified Date:", drive["lastModifiedDateTime"])
print("\n")


# Get drive items
# site_id = "d659b49c-9e0d-4cc4-95bb-4cc377a2d8ba"
drive_id = "b!nLRZ1g2exEyVu0zDd6LYuqbIIh75Y7ZKhoLRLGvwXzVXewcZecd-R6CP5rCPiYSu"
graph_url = 'https://graph.microsoft.com/v1.0/drives/' + drive_id + '/items/root/children'
items = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
for item in json.loads(items.content)["value"]:
    print(" Item")
    print("   Name:", item["name"])
    print("   Id:", item["id"])
    print("   Web Url:", item["webUrl"])
    print("   Created Date:", item["createdDateTime"])
    print("   Last Modified Date:", item["lastModifiedDateTime"])
    print("   Size:", item["size"])
    print("   File:", item["file"])
    # print("   @microsoft.graph.downloadUrl:", item["@microsoft.graph.downloadUrl"])
    print("   Parent Reference siteId:", item["parentReference"]["siteId"])
    
print("\n")


# Download drive document
drive_id = "b!nLRZ1g2exEyVu0zDd6LYuqbIIh75Y7ZKhoLRLGvwXzVXewcZecd-R6CP5rCPiYSu"
item_id = "013F3BRVPPJNKJ3NRY4ZDY4TJQ6ZD7LLGH"
item_id = "013F3BRVJEEKKHCCUVP5FZFZX3CZ2FZACW"
print("Getting drive item...")
graph_url = 'https://graph.microsoft.com/v1.0/drives/' + drive_id + '/items/' + item_id 
item = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
item_name = json.loads(item.content)["name"]
print("Downloading document...")
graph_url = 'https://graph.microsoft.com/v1.0/drives/' + drive_id + '/items/' + item_id + '/content'
item = requests.get(graph_url, headers={'Authorization': 'Bearer {0}'.format(token)})
with open("./" + item_name, 'wb') as f:
    f.write(item.content)    
    print("Document downloaded to: ", f.name)

print("\n")

