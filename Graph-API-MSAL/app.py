import requests
import json
import msal
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
print( config.get('azure','clientId'))

client_id = config.get('azure','clientId')
client_secret = config.get('azure','clientSecret')
authority = "https://login.microsoftonline.com/" + config.get('azure','tenantId')
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

# The pattern to acquire a token looks like this.
result = None

# First, the code looks up a token from the cache.
# Because we're looking for a token for the current app, not for a user,
# use None for the account parameter.
result = app.acquire_token_silent(scope, account=None)

if not result:
    print("No suitable token exists in cache. Let's get a new one from Azure AD.")
    result = app.acquire_token_for_client(scopes=scope)

if "access_token" in result:
    # Call a protected API with the access token.
    print(result["token_type"])
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You might need this when reporting a bug.


http_headers = {'Authorization': 'Bearer ' + result['access_token'],
                'Accept': 'application/json',
                'Content-Type': 'application/json'}

graph_url = 'https://graph.microsoft.com/v1.0/sites/root'

site = requests.get(
    graph_url,
    headers=http_headers
).json()

print(site)
print(site["webUrl"])

