import requests
from urllib.parse import urlencode

from airtable.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError

class Client(object):
    URL = "https://api.airtable.com/"
    AUTH_URL = "https://airtable.com/oauth2/v1/"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, access_token=None, client_id=None, client_secret=None, redirect_uri=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri

    def authorization_url(self, state, code_challenge):
        auth_endpoint = "authorize?"
        params = {
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI,
            'response_type': 'code',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'scope': 'data.records:read data.records:write'
        }
        return self.AUTH_URL + auth_endpoint + urlencode(params)

    def token_creation(self, code, code_verifier):
        headers= {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.CLIENT_ID}:{self.CLIENT_SECRET}"
        }
        body = {
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
            "grant_type": "authorization_code",
            "code_verifier": code_verifier,
            "code_challenge_method": "S256"
        }
        return self.post('token', data=body, headers=headers, auth_url=True)

    def refresh_token(self, refresh_token):
        headers= {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.CLIENT_ID}:{self.CLIENT_SECRET}"
        }
        body = {
            "grant_type": "authorization_code",
            "refresh_token": refresh_token,
        }
        return self.post('token', data=body, headers=headers, auth_url=True)

    def get(self, endpoint, params=None):
        response = self.request('GET', endpoint, params=params)
        return self.parse(response)

    def post(self, endpoint, params=None, data=None, headers=None, json=True, auth_url=False):
        response = self.request('POST', endpoint, params=params, data=data, headers=headers, json=json, auth_url=auth_url)
        return self.parse(response)

    def delete(self, endpoint, params=None):
        response = self.request('DELETE', endpoint, params=params)
        return self.parse(response)

    def request(self, method, endpoint, params=None, data=None, headers=None, json=True, auth_url=False):
        _headers = self.headers
        if headers:
            _headers.update(headers)
        kwargs = {}
        if json:
            kwargs['json'] = data
        else:
            kwargs['data'] = data
        if auth_url:
            return requests.request(method, self.AUTH_URL + endpoint, params=params, headers=_headers, **kwargs)
        else:
            return requests.request(method, self.URL + endpoint, params=params, headers=_headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
