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

### Get access_token
To get the access token using Oauth2 follow the next steps:
Check https://airtable.com/developers/web/api/oauth-reference for more info.

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