https://docs.databricks.com/aws/en/dev-tools/python-sql-connector#:~:text=from%20databricks.,as%20connection%3A

# Add a Databricks SQL Warehouse

Add a sql-warehouse service to the FastAPI app that connects to a databricks SQL warehouse using m2m auth like in the link.
Note, you will need to construct the HTTP_PATH yourself from the warehouse id
add a button on the homepage that queries 'SELECT CURRENT_TIMESTAMP()' from the warehouse to test it, then displays the result in the UI.

use DATABRICKS_HOST and the DATABRICKS_WAREHOUSE_ID to construct the warehouse's endpoint, instead of SERVER_HOSTNAME or HTTP_PATH which the docs use. note DATABRICKS_HOST already has the https:// at the front.

## code sample from website for M2M auth. note, our setup slightly differs, as mentioned above

```python
from databricks.sdk.core import Config, oauth_service_principal
from databricks import sql
import os

server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")

def credential_provider():
    config = Config(
        host = f"https://{server_hostname}",
        client_id = os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret = os.getenv("DATABRICKS_CLIENT_SECRET"))
    return oauth_service_principal(config)

with sql.connect(
    server_hostname = server_hostname,
    http_path = os.getenv("DATABRICKS_HTTP_PATH"),
    # Take special care to notice credentials_provider is a parameter that takes the function credential_provider as an argument. Not the output of credential_provider, but the function is the argument.
    credentials_provider = credential_provider) as connection:
        # this connection should be stored
```
