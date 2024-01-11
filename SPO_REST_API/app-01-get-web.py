# WIP...
from office365.sharepoint.client_context import ClientContext
from appsecrets import test_client_id, test_client_secret, test_site_url

ctx = ClientContext(test_site_url).with_client_credentials(
    test_client_id, test_client_secret
)
target_web = ctx.web.get().execute_query()
print(target_web.url)
print(target_web.created)

