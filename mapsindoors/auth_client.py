import requests
import json
from mapsindoors.url_classes import *

class OAuthToken:
    def __init__(self, username, password, api_key):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.access_token = self.get_access_token()
        self.url = Urls(api_key, response_format="json")
            
    def get_access_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = 'https://auth.mapsindoors.com/connect/token'
        payload = {'client_id': 'client', 'username': self.username, 'grant_type': 'password', 'password': self.password}
        response = requests.post(url=url, data=payload, headers=headers)
        data = response.json()['access_token']
        bearer_token = 'Bearer ' + data
        return bearer_token