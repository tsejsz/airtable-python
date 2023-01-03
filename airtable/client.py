import requests
from urllib.parse import urlencode
import hashlib
import base64

from airtable.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.airtable.com/v0/"
    AUTH_URL = "https://airtable.com/oauth2/v1/"

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, code_verifier=None):
        """
        client_id: get it from https://airtable.com/create/oauth
        client_secret: get it from https://airtable.com/create/oauth
        code_verifier:
        Must be a cryptographically generated string; 43-128 characters long.
        Characters belong to the set: a-z / A-Z / 0-9 / “.” / “-” / “\_”.
        """
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri
        self.CODE_VERIFIER = code_verifier
        self.token = None
        if client_id and client_secret:
            self.CREDENTIALS = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()).decode()

    def authorization_url(self, state):
        code_challenge = (
            base64.b64encode(hashlib.sha256(self.CODE_VERIFIER.encode()).digest())
            .decode()
            .replace("=", "")
            .replace("+", "-")
            .replace("/", "_")
        )
        auth_endpoint = "authorize?"
        params = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": self.REDIRECT_URI,
            "response_type": "code",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "scope": "data.records:read data.records:write schema.bases:read",
        }
        return self.AUTH_URL + auth_endpoint + urlencode(params)

    def token_creation(self, code):
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {self.CREDENTIALS}"}
        body = {
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
            "code_verifier": self.CODE_VERIFIER,
            "code_challenge_method": "S256",
            "grant_type": "authorization_code",
        }
        return self.post("token", data=body, headers=headers, auth_url=True)

    def refresh_token(self, refresh_token):
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {self.CREDENTIALS}"}
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        return self.post("token", data=body, headers=headers, auth_url=True)

    def get_current_user(self):
        return self.get("meta/whoami")

    def list_bases(self):
        return self.get("meta/bases")

    def list_base_tables(self, baseId):
        return self.get(f"meta/bases/{baseId}/tables")

    def set_token(self, token):
        self.token = token

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, headers=None, auth_url=False, **kwargs):
        _headers = {
            "Accept": "application/json",
        }
        if self.token:
            _headers["Authorization"] = "Bearer " + self.token["access_token"]
        if headers:
            _headers.update(headers)
        if "Content-Type" not in _headers:
            _headers["Content-Type"] = "application/json"
        if auth_url:
            return requests.request(method, self.AUTH_URL + endpoint, headers=_headers, **kwargs)
        else:
            return requests.request(method, self.URL + endpoint, headers=_headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
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
