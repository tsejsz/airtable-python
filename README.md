# airtable-python

*airtable-python* is an API wrapper for Airtable, written in Python
- Use this library if you are interested in Oauth authentication and webhook notifications.

## Installing
```
pip install airtable-python
```
## Usage
```
from airtable.client import Client
client = Client(client_id, client_secret, redirect_uri, code_verifier)
```
*Note: If you already have an access token, you can initiate Client without any parameters and directly set token with the access token you have as a dictionary {"access_token": token}*
### Get access_token
To get the access token using Oauth2 follow the next steps.
Check https://airtable.com/developers/web/api/oauth-reference for more info:

1. Get authorization URL to receive code
```
url = client.authorization_url(state)
```
2. Get access token using code
```
token = client.token_creation(code)
```
3. Set access token
```
client.set_token(access_token)
```
If your access token expired, you can get a new one using refresh_token:
```
response = client.refresh_access_token(refresh_token)
```
And then set access token again...  


### Get current user
```
user = client.get_current_user()
```
### List Bases
```
bases = client.list_bases()
```
### List Tables
```
tables = client.list_base_tables(baseId)
```
### List records
```
records = client.list_records(
    baseId, 
    tableId, 
    pageSize=None, 
    maxRecords=None, 
    filter_field=None, 
    filter_value=None, 
    sort_field=None, 
    sort_direction=None
)
# baseId and tableId are required
# sort_direction options are 'desc' or 'asc'
```
### Create Records
```
records = [
    {
        "fields": {
          "Projects": "Project from python",
          "Status": "In progress",
          "Complete?": False
        }
    },
]
records = client.create_records(baseId, tableId, records)
```
### Update Record
```
data = {
    "Status": "Complete",
    "Complete?": True
}
record = client.update_record(baseId, tableId, recordId, data)
```
### List Collaborators (needs enterprise scopes access)
```
collabs = client.list_collaborators(baseId)
```
