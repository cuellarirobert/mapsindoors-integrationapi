import requests
import json
from mapsindoors.integration_api_instance import api_instance
from mapsindoors.url_classes import *


class AppUserRoles:
	def __init__(self, app_user_roles_dict):
		self.id = app_user_roles_dict['id']
		self.names = app_user_roles_dict['names']
		self.language_code = app_user_roles_dict['names'][0]['language']