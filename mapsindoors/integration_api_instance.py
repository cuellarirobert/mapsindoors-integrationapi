import requests
import json
from mapsindoors.url_classes import *
from mapsindoors.geodata import *

class ApiInstance:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = Urls(api_key, response_format="json")

    def get_app_user_roles(self):
    	response = requests.request("GET", url=self.url.app_user_roles_url(), headers={'Accept': 'application/json'})
    	return response.json()

    #returns the full datasest for all geodata objects in a solution
    def get_raw_geodata(self):
    	response = requests.request("GET", url=self.url.geodata_url(), headers={'Accept': 'application/json'})
    	return response.json()

    def get_location_types(self):
        response = requests.request("GET", url=self.url.display_types_url(), headers={'Accept': 'application/json'})
        return response.json()

    def get_categories(self):
        response = requests.request("GET", url=self.url.categories_url(), headers={'Accept': 'application/json'})
        return response.json()
