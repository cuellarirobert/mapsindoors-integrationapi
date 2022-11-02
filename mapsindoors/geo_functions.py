from mapsindoors.geodata import *
from mapsindoors.integration_api_instance import *
from mapsindoors.auth_client import *
from mapsindoors.url_classes import *
import requests
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import radians, cos, sin, asin, sqrt
import pyproj
from shapely.ops import transform
import re
import os


# api = api_instance('your user name', 'YOURPASSWORD', 'api key')


class GeoFunctions:
    def __init__(self, username, password, api_key):
        """
        instance: gets authorization
        geodata_response: list of dictionaries of all geodata
        location_types : list of dictionaries of location types
        categories: list of dictionaries of categories
        app_user_roles: list of dictionaries of app_user_roles. AppUserRoles class can be used for dot notation.  requires import of app_user_roles module.
        url makes available all url's from the url_classes file.
        access_token is the OAuthToken bearer token
        geodata_objects is the (list of objects) dot notation form of the geodata response.
        """

        self.instance = ApiInstance(username, password, api_key)
        self.api_key = api_key
        self.geodata_response = self.instance.get_raw_geodata()
        self.location_types = self.instance.get_location_types()
        self.categories = self.instance.get_categories()
        self.app_user_roles = self.instance.get_app_user_roles()
        self.url = Urls(api_key)
        self.access_token = self.instance.access_token
        geodata_objects = []
        for item in self.geodata_response:
            geodata_objects.append(Geodata(item))
        self.geodata_objects = geodata_objects
    

    #returns a specific location, and creates an object to be used in dot notation.  e.g. location.id instead of location['id']
    def get_location(self, location_id:str, json:bool=False):
        """
        Gets a location based on the MapsIndoors internal Id. Can be found in the CMS.
        Locations may be one of 'Venue', 'Building', 'Floor', 'poi', 'area', 'room'.

        Parameters
        ----------
        location_id --> string
        json --> specifies to return an object or a json dict (default --> object)

        Returns
        -------

        location object if json=False. can then return things like location.id or location.externalId, location.properties.name.en, etc.

        examples
        -------

        get_location('a4394d6ec46d4060888652cb', json=False)
        get_location('a4394d6ec46d4060888652cb', json=True)
        """
        for item in self.geodata_response:
            if item['id'] == location_id:
                if json == False:
                    return(Geodata(item))
                elif json == True:
                    return(item)

    def get_location_by_external_id(self, external_id:str, json:bool=False):
        """
        Gets a location based on the MapsIndoors external Id. Can be found in the CMS.
        Locations may be one of 'Venue', 'Building', 'Floor', 'poi', 'area', 'room'.

        Parameters
        ----------
        external_id --> string
        json --> specifies to return an object or a json dict (default --> object)

        Returns
        -------

        location object if json=False. can then return things like location.id or location.externalId, location.properties.name.en, etc.

        examples
        -------

        get_location_by_external_id('1.07.01a', json=False)
        get_location_by_external_id('1.07.01a', json=True)
        """

        self.external_id = external_id
        locations = []
        for i in self.geodata_response:
            try:
                 if i['externalId'].lower() == external_id.lower():
                    if json == False:
                        locations.append(Geodata(i))
                    elif json == True:
                        locations.append(i)
            except KeyError:
                continue
        return locations

    def get_user_role_name_by_id(self, user_role_id:str, language_symbol:str):
        for item in self.app_user_roles:
            if item['id'] == user_role_id:
                for name in item['names']:
                    if name['language'] == language_symbol:
                        return name['name']


        
    def get_locations_by_alias(self, alias:str, json:bool=False):
        """
        Gets a location based on the MapsIndoors Alias. Can be found in the CMS.
        Locations may be one of 'Venue', 'Building', 'Floor', 'poi', 'area', 'room'.

        Parameters
        ----------
        Alias --> string
        json --> specifies to return an object or a json dict (default --> object)

        Returns
        -------

        location object if json=False. can then return things like location.id or location.externalId, location.properties.name.en, etc.

        examples
        -------

        get_location_by_alias('1.07.01a', json=False)
        get_location_by_alias('1.07.01a', json=True)
        """
        self.alias = alias.upper()
        locations = []
        for i in self.geodata_response:
            try:
                if i['aliases'] != []:
                    for item in i['aliases']:
                        if item.upper() == alias.upper():
                            if json == False:
                                locations.append(Geodata(i))
                            elif json == True:
                                locations.append(i)
            except KeyError:
                continue
        return locations

    #because the items in the geodata response only contain a location type id (display type id), it's useful to get the id from the name.  this value is not actually visible in the CMS at all.
    def get_location_type_id(self, location_type_name:str):
        """
        Gets an id of a location type based on the name. The geoJson does not contain the name, only the id. 

        Parameters
        ----------
        location_type_name --> string --> not case sensitive and white spaces are allowed.

        Returns
        -------

        location type id.  this is also referred to as a display type id in other contexts.

        examples
        -------

        get_location_type_id('meeting room')
        """
        self.location_type_name = location_type_name.replace(" ", "_").lower()
        for item in self.location_types:
            if item['name'].replace(" ", "_").lower() == self.location_type_name:
                return(item['id'])

    #similar to the get_location_type_id, but will return the location type name in the format that the database has it.  this can help if the user tries to search via a name (like one found in the CMS).
    def get_location_type_administrative_id(self, location_type_name:str):
        """
        Gets an id of a location type based on the name. Can be used in get_locations function. 

        Parameters
        ----------
        location_type_name --> string --> not case sensitive and white spaces are allowed.

        Returns
        -------

        location type id.  this is also referred to as a display type id in other contexts.

        examples
        -------

        get_location_type_administrative_id('meeting room')
        """
        self.location_type_name = location_type_name.replace(" ", "_").lower()
        for item in self.location_types:
            item['name'] = item['name'].lower()
            if item['name'] == self.location_type_name:
                return(item['name'])

    #generally not needed as you can use get_locations, however if you have the location_type_id you can also search from it with this method.
    def get_locations_by_display_type_id(self, location_type_id:str, json:bool=False):
        """
        Gets all locations of a particular display type/location type 'id'. get_locations() can use the location_type adminimistrative id, which is different than the 'id'. 

        Parameters
        ----------
        location_type_id --> string --> looks like a hashed id.
        json --> True returns json.  False returns json in integration Api geojson format.

        Returns
        -------

        a list of locations either as objects or as geojson based on the json parameter.

        examples
        -------

        get_locations_by_display_type_id('a0c8d3faff9a406c977592f0')
        get_locations_by_display_type_id('a0c8d3faff9a406c977592f0', json=True)
        """
        display_type_locations_list = []
        self.location_type_id = location_type_id
        for item in self.geodata_response:
            if item['baseType'] not in ('venue', 'building', 'floor') and item['displayTypeId'] == location_type_id:
                if json == False:
                    display_type_locations_list.append(Geodata(item))
                elif json == True:
                    display_type_locations_list.append(item)
        return display_type_locations_list

    #items in the geodata contain only a category id. if you know the category key this can fetch the id.
    def get_category_id(self, category_name:str, language_symbol:str):
        """
        Gets the category 'id' from a category name.

        Parameters
        ----------
        category_name --> name
        language_symbol --> e.g. 'en', 'da', 'de', etc.

        Returns
        -------

        returns a category 'id'

        examples
        -------

        get_category_id('IoT devices', language_symbol='en')
        get_category_id('IoT enheder', language_symbol='da')

        """
        self.category_name = category_name.lower()
        for item in self.categories:
            if category_name.lower() == item['name'][language_symbol].lower():
                return(item['id'])

    def get_category_name(self, category_id:str, language_symbol:str):
        """
        Gets the category 'name' from a category id.

        Parameters
        ----------
        category_id --> id
        language_symbol --> e.g. 'en', 'da', 'de', etc.

        Returns
        -------

        returns a category 'name'

        examples
        -------

        get_category_name('105241f501d940b4af1aede8', language_symbol='en')
        get_category_name('105241f501d940b4af1aede8', language_symbol='da')

        """
        self.category_id = category_id
        for item in self.categories:
            if category_id == item['id']:
                return(item['name'][language_symbol])

    def get_location_type_name(self, location_type_id:str):
        """
        Gets the location 'name' from a location type ID (displayTypeId)

        Parameters
        ----------
        location_type_id --> id
        
        Returns
        -------

        returns a location type 'name'

        examples
        -------

        get_location_type_name('105241f501d940b4af1aede8')


        """
        self.location_type_id = location_type_id
        for item in self.location_types:
            if item['id'] == location_type_id:
                return(item['name'])

    #get_locations does not contain buildings, so use this to get the buildings in a venue. similar to get_child_objects with a venue, but this will exclude outside POIs/areas.
    def get_buildings_in_venue(self, venue_id:str, json:bool=False):
        """
        returns a list of buildings

        Parameters
        ----------
        venue_id --> string
        json --> specifies to return an object or a json dict (default --> object)

        Returns
        -------

        list of buildings.  objects or id's based on json parameter.

        examples
        -------

        get_buildings_in_venue('b8ce325e29444d76a32fbf55', json=False)
        get_buildings_in_venue('b8ce325e29444d76a32fbf55', json=True)
        """
        locations_list = []
        venue_child_objects = self.get_child_objects(venue_id)
        for item in venue_child_objects:
            if item['baseType'] == 'building':
                if json == False:
                    item = Geodata(item)
                    locations_list.append(item)
                elif json == True:
                    locations_list.append(item)
        return locations_list

    #this will get only the outside poi and areas for a particular venue.
    def get_outside_poi_and_area(self, venue_id, json:bool=False):
        """
        returns a list of outside locations not inside a building

        Parameters
        ----------
        venue_id --> string
        json -> False returns geodata objects, true will return the JSON data
        

        Returns
        -------

        list of outside locations.

        examples
        -------

        get_outside_poi_and_area('b8ce325e29444d76a32fbf55', json=False)
        get_outside_poi_and_area('b8ce325e29444d76a32fbf55', json=True)
        
        """
        locations_list = []
        venue_child_objects = self.get_child_objects(venue_id)
        for item in venue_child_objects:
            if item['baseType'] == 'poi' or item['baseType'] == 'area':
                if json == False:
                    item = Geodata(item)
                    locations_list.append(item)
                elif json == True:
                    locations_list.append(item)
        return locations_list

    #gets all floors in a building.  can also use get_child_objects method on a building id for the same result.
    def get_floors_in_building(self, building_id):
        locations_list = []
        building_child_objects = self.get_child_objects(building_id)
        for item in building_child_objects:
            if item['baseType'] == 'floor':
                item = Geodata(item)
                locations_list.append(item)
        return locations_list



    def get_location_venue_id(self, location_id):
        """
        Gets the venue id of a location. Works with locations inside building or outside.
        baseType venue has geodata parent. 

        Parameters
        ----------
        location_id --> mapsindoors location id

        Returns
        -------

        returns a venue 'id'

        examples
        -------

        get_location_venue_id('3dbe1a2e7c364732a2ae6cb1')

        """
        for item in self.geodata_response:
            if item['id'] == location_id:
                item = Geodata(item)
                try:
                    direct_parent = self.get_location(item.parentId)
                    if direct_parent.baseType == 'floor':
                        building = self.get_location(direct_parent.parentId)
                        venue = self.get_location(building.parentId)
                        return venue.id
                    elif direct_parent.baseType == 'venue':
                        return direct_parent.id
                except AttributeError:
                    return 'Cannot use a venue id.'
                

    def get_child_objects(self, location_id:str, json:bool=True):
        """
        Checks locations to see if a parent exists with the location_id.
        baseType should be floor, building or venue.

        Parameters
        ----------
        location_id --> mapsindoors internal id.
        json --> True returns json items, False returns geodata objects.  True is default

        Returns
        -------

        returns a list of locations that match the criteria.

        examples
        -------

        get_child_objects('77eac43db1094a40add4f0b6')

        """
        child_object_list = []
        for item in self.geodata_response:
                try:
                    if item['parentId'] == location_id:
                        if json == True:
                            child_object_list.append(item)
                        if json == False:
                            item = Geodata(item)
                            child_object_list.append(item)
                except KeyError:
                    continue
        return child_object_list



    #math for getting distance between two points on Earth
    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Gets distance between two coordinate pairs. 

        Parameters
        ----------
        lon1 --> longitude1
        lat1 --> latitude1
        lon2 --> longitude2
        lat2 --> latitude2


        Returns
        -------

        returns a distance in meters.


        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r * 1000

    def get_distance(self, location_id_1:str, location_id_2:str, unit:str='feet'):
        """
        returns a distance based on two locations.  does not account for height if floors are different.  can be any kind of geo object and will use the anchor points.

        Parameters
        ----------
        location_id_1 --> mapsindoors id of location
        location_id_2 --> mapsindoors id of location
        unit --> 'meters' or 'feet'

        Returns
        -------

        returns distance.

        examples
        -------

        get_distance('8d9b21b028df40e38f8c52d7', '7c841c82151247978dde13d9' unit='meters')
        get_distance('8d9b21b028df40e38f8c52d7', '7c841c82151247978dde13d9')
        get_distance('8d9b21b028df40e38f8c52d7', '7c841c82151247978dde13d9' unit='feet')

        """
        try:
            location1 = self.get_location(location_id_1, json=True)
            location2 = self.get_location(location_id_2, json=True)

            lat1 = location1['anchor']['coordinates'][1]
            lon1 = location1['anchor']['coordinates'][0]
            lat2 = location2['anchor']['coordinates'][1]
            lon2 = location2['anchor']['coordinates'][0]

            distance_meters = self.haversine(lon1, lat1, lon2, lat2)
            if unit == 'meters':
                return distance_meters
            elif unit == 'feet':
                return distance_meters * 3.28084
        except IndexError:
            return 'One or more locations does not exist.'


    
    def get_polygons(self, json:bool=True):
        """
        gets all areas for a given API key.  can also use get_locations, but that method can only return one baseType at a time.
        it does however provide the ability to query for multiple features like location types, categories, names etc.

        Parameters
        ----------
        json --> True or False.  Default is True
        

        Returns
        -------

        Returns a list of locations with baseType 'area' or 'room'. Format as objects or json specified by the json boolean parameter.

        examples
        -------

        get_polygons(json=True)
        get_polygons(json=False)
        
        """
        polygon_list = []
        geodata = self.geodata_response
        for item in geodata:
            if item['baseType'] == 'area' or item['baseType'] == 'room':
                if json == True:
                    polygon_list.append(item)
                elif json == False:
                    polygon_list.append(Geodata(item))
        return polygon_list
    
    def get_venues(self, json:bool=True):
        """
        gets all venues for a given API key.  a alternative method to get_locations.

        Parameters
        ----------
        json --> True or False.  Default is True
        

        Returns
        -------

        Returns a list of geojson objects with baseType 'venue'. Returned as geodata objects or json specified by the json boolean parameter.

        examples
        -------

        get_venues(json=True)
        get_venues(json=False)
        
        """
        venue_list = []
        for item in self.geodata_response:
            if item['baseType'] == 'venue':
                if json == True:
                    venue_list.append(item)
                elif json == False:
                    venue_list.append(Geodata(item))
        return venue_list

    def get_location_floor_index(self, location_id):
        """
        the floor index for a location (poi/area/room) cannot be found directly on the metadata of the location.
        this data is found on the parent if inside a building.

        Parameters
        ----------
        location_id.  location baseType allowed includes poi, area, room.
        

        Returns
        -------

        Returns the floor index of the parent floor of a location.

        examples
        -------

        get_location_floor_index(location_id='a4394d6ec46d4060888652cb')
        
        """
        self.location_id = location_id
        location = self.get_location(self.location_id)
        if location.baseType == 'room' or location.baseType == 'area' or location.baseType == 'poi':
            parent_object = self.get_location(location.parentId)
        else:
            return "Location is not one the following baseType: 'area', 'poi', 'room'"
        if parent_object.baseType == 'floor':
            return parent_object.baseTypeProperties.administrativeid
        elif location.baseType == 'venue':
            return 'Location is not inside of building polygon. Parent is venue.'



    def geodesic_point_buffer(self, lat, lon, m):
        proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')
        aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
        project = partial(
            pyproj.transform,
            pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
            proj_wgs84)
        buf = Point(0, 0).buffer(m)  # distance in meters
        circle = transform(project, buf).exterior.coords[:]
        circle = circle[0:-1]
        return [list(x) for x in circle]


    def bounding_box(self, points):
        """
        used in the circle functions
        """
        bot_left_x = min(point[0] for point in points)
        bot_left_y = min(point[1] for point in points)
        top_right_x = max(point[0] for point in points)
        top_right_y = max(point[1] for point in points)
        return list(eval((re.sub(r"\((.*?)\)", r"\1", str([(bot_left_x, bot_left_y), (top_right_x, top_right_y)])[1:-1]))))


    def get_areas_within_radius(self, location_id, radius_meters):
        new_location = self.get_location(location_id)
        define_radius_of_location = self.geodesic_point_buffer(new_location.anchor.coordinates[1], new_location.anchor.coordinates[0], radius_meters)
        targeted_area_list_tuples = list(tuple(x) for x in define_radius_of_location)
        targeted_area = Polygon(targeted_area_list_tuples)
        venue_id_list = []
        venues = self.get_venues()
        for item in venues:
            venue_id_list.append(item['id'])
        parent_list = []
        polygon_list = self.get_polygons()
        for item in polygon_list:
            if (item['parentId'] == new_location.parentId) or (item['parentId'] in venue_id_list):
                polygon_shape = (item['geometry']['coordinates'][0][:-1])
                shapely_polygon_area = self.convert_polygon_to_shapely_polygon(polygon_shape)
                if targeted_area.intersects(shapely_polygon_area) == True:
                    parent_list.append(f"{item['id']}, {item['properties']['name@en']}")
        else:
            pass
        return parent_list

    def convert_polygon_to_shapely_polygon(self, polygon_coordinates_list_of_lists):
        self.area_coordinates_tuples = list(tuple(x) for x in polygon_coordinates_list_of_lists)
        area_shapely = Polygon(self.area_coordinates_tuples)
        return area_shapely

