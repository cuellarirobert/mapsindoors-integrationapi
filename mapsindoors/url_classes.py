class Urls:
    def __init__(self, api_key, response_format="json"):
        self.format = response_format
        self.api_key = api_key
        self.base_url = f"https://integration.mapsindoors.com/{api_key}/api/"
        self.app_user_roles = "appUserRoles"
        self.categories = "categories"
        self.dataset = "dataset"
        self.geodata = "geodata"
        self.display_types = "displaytypes"
        
    def base_url(self):
        return self.base_url
    
    def app_user_roles_url(self):
        return self.base_url + self.app_user_roles

    def categories_url(self):
        return self.base_url + self.categories
    
    def dataset_url(self):
        return self.base_url + self.dataset
    
    def display_types_url(self):
        return self.base_url + self.display_types
    
    def geodata_url(self):
        return self.base_url + self.geodata
    
  
    





