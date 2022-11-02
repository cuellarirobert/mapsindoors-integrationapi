import json
from mapsindoors.integration_api_instance import *

class Geodata:
	def __init__(self, json_dict):
		"""
		class properties

		documentation can also be found @ https://docs.mapsindoors.com/api/

Id

All elements have a unique 24 character string.

If you are creating, this should be null, since it will be generated upon saving the object.

ParentId
For elements (other than the root) there is a parentId which links to the element it's connected to.
This will be a 24 character string, just as Id is.

BaseType
Tells what kind of data it is - it can be poi, room, area, floor, building, or venue.

BaseTypeProperties
Defines a dictionary setup with properties that is bound by its BaseType.
It is not possible to add any other keys to BaseTypeProperties, except the predefined ones.

DisplayTypeId
Is a reference to the display type as described below. All rooms and poi geodata requires this to be set. As this is an ID, the reference is a 24 character string format as described above.

Geometry
Contains the actual geodata - where it is on the map. It's based on GeoJSON - in the example above the geometry is a point defining the POIs position on the map.

Aliases
Is an optional list of aliases for this data written as a list of non-translated text. This can be used e.g. if a building or room has a common nickname users could use when searching for it.

Categories
Is a reference to the category data as described below. Geodata is not required to reference any categories - like in this example. As this is an ID, the reference is a 24 character string as described above.

Status
Is a bitfield.
bit1: active. If an element is not active, it will not be given to the apps.
bit2: searchable. If an element is not searchable it might be shown on the map, but not show up in searches.
As there are two bits, the final values can be:
0: Not active, Not searchable 1: active, Not searchable 2: Not active, searchable (not a very useful combo) 3: active, searchable

Properties
Contains other data about the Geodata object such as names, description or even custom data like gate numbers, vendor id, exhibition id or other data needed.
Name is mandatory - at least for the base language set for the dataset.

The key format is: @

E.g. name in english will be ‘name@en' - in the example with a value of "Coat stand (RT)"

As this is a dictionary setup, the keyname needs to be unique and only contain the ascii chars [a-z] and [0-9]. Use of spaces and unicode chars here is discouraged as it makes it harder to use from the application code side. The char @ is not supported in the keyname as it's used as a seperator. As an example, if you want to store opening hours here you could use the key openinghours@en as a keyname.




		"""
		self.geodata = json_dict
		self.id = json_dict['id']

		
		try:
			self.parentId = json_dict['parentId']
		except KeyError:
			pass
		
		self.datasetId = json_dict['datasetId']
		
		try:
			self.externalId = json_dict['externalId']
		except KeyError:
			pass
		
		self.baseType = json_dict['baseType']
		
		try:
			self.displayTypeId = json_dict['displayTypeId']
		except KeyError:
			pass

		try:
			self.displaySetting = GeodataField(json_dict['displaySetting'])
		except KeyError:
			pass
		except AttributeError:
			pass# except 
		
		self.geometry = Geometry(json_dict['geometry'])
		
		try:
			self.anchor = Anchor(json_dict['anchor'])
		except KeyError:
			pass
		
		try:
			self.aliases = json_dict['aliases']
		except KeyError:
			pass

		try:
			self.categories = json_dict['categories']
		except KeyError:
			pass

		try:
			self.tileStyles = json_dict['tileStyles']
		except KeyError:
			pass

		try:
			self.tilesUrl = json_dict['tilesUrl']
		except KeyError:
			pass
		
		self.status = json_dict['status']
		
		self.baseTypeProperties = BaseTypeProperties(json_dict['baseTypeProperties'])

		# self.properties = json_dict['properties']


		self.props = Properties(json_dict['properties'])

		self.properties = GeodataField(self.props.props)



class Geometry:
	def __init__(self, geometry_dict):
		self.coordinates = geometry_dict['coordinates'][0]
		try:
			self.bbox = geometry_dict['bbox']
		except KeyError:
			pass
		self.type = geometry_dict['type']

class BaseTypeProperties:
	def __init__(self, baseTypeProperties_dict):
		try:
			self.defaultfloor = baseTypeProperties_dict['defaultfloor']
		except KeyError:
			pass
		try:
			self.name = baseTypeProperties_dict['name']
		except KeyError:
			pass
		self.administrativeid = baseTypeProperties_dict['administrativeid']
		try:
			self.graphid = baseTypeProperties_dict['graphid']
		except KeyError:
			pass
		try:
			self.capacity = baseTypeProperties_dict['capacity']
		except KeyError:
			pass
		try:
			self.Class = baseTypeProperties_dict['class']
		except KeyError:
			pass

class Anchor:
	def __init__(self, anchorDict):
		self.coordinates = anchorDict['coordinates']
		self.lat = anchorDict['coordinates'][1]
		self.lon = anchorDict['coordinates'][0]
		self.type = anchorDict['type']

class Properties:
	def __init__(self, properties_dict):
		self.props = {}
		# print(propertiesDict)
		for key in properties_dict.keys():
			if '@' in key:
				[prop, language] = key.split('@')
				if prop not in self.props:
					self.props[prop] = {}
				if language not in self.props[prop]:
					self.props[prop][language] = {}
					self.props[prop][language] = properties_dict[key]
			else:
				self.props[key] = properties_dict[key]


class GeodataField(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)

        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = GeodataField(value)
            self.__dict__[key] = value

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if type(value) is GeodataField:
                value = value.to_dict()
            d[key] = value
        return d

    def __repr__(self):
        return str(self.to_dict())

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]


# newExample = {
#     "id": "b8ce325e29444d76a32fbf55",
#     "datasetId": "328dd35ea5aa40748a34341f",
#     "externalId": "",
#     "baseType": "venue",
#     "geometry": {
#       "coordinates": [
#         [
#           [
#             -97.7323435,
#             30.3803273
#           ],
#           [
#             -97.7327619,
#             30.3805127
#           ],
#           [
#             -97.7323192,
#             30.3812552
#           ],
#           [
#             -97.7334578,
#             30.3817609
#           ],
#           [
#             -97.7334064,
#             30.3819004
#           ],
#           [
#             -97.730425,
#             30.3805373
#           ],
#           [
#             -97.7304725,
#             30.3803814
#           ],
#           [
#             -97.731882,
#             30.3810526
#           ],
#           [
#             -97.7323435,
#             30.3803273
#           ]
#         ]
#       ],
#       "bbox": [
#         -97.7334578,
#         30.3803273,
#         -97.730425,
#         30.3819004
#       ],
#       "type": "Polygon"
#     },
#     "anchor": {
#       "coordinates": [
#         -97.7320766395617,
#         30.3811538835
#       ],
#       "type": "Point"
#     },
#     "aliases": [],
#     "status": 3,
#     "baseTypeProperties": {
#       "defaultfloor": "0",
#       "administrativeid": "AUSTIN",
#       "graphid": "AUSTIN_Graph"
#     },
#     "properties": {
#       "name@en": "Austin Office",
#       "name@da": "Austin Kontor"
#     },
#     "tilesUrl": "https://tiles.mapsindoors.com/tiles/indoor/mapspeopleoffice/29/{style}/l{floor}/z{z}/x{x}/y{y}.png",
#     "tileStyles": [
#       {
#         "displayName": "default",
#         "style": "default"
#       }
#     ]
#   }



# example = {
#    "id":"5a770ca89fe54561bbbd5434",
#    "parentId":"77eac43db1094a40add4f0b6",
#    "datasetId":"328dd35ea5aa40748a34341f",
#    "baseType":"area",
#    "displayTypeId":"d560b3f4708e470a9ff4a803",
#    "displaySetting":{
#       "name":"default",
#       "polygon":{
#          "visible": True,
#          "strokeWidth":0.0,
#          "fillColor":"#1E90FF",
#          "fillOpacity":0.45
#       }
#    },
#    "geometry":{
#       "coordinates":[
#          [
#             [
#                9.950304,
#                57.058222
#             ],
#             [
#                9.950488,
#                57.058024
#             ],
#             [
#                9.950654,
#                57.057892
#             ],
#             [
#                9.951035,
#                57.057983
#             ],
#             [
#                9.950984,
#                57.058104
#             ],
#             [
#                9.950304,
#                57.058222
#             ]
#          ]
#       ],
#       "bbox":[
#          9.950304,
#          57.057892,
#          9.951035,
#          57.058222
#       ],
#       "type":"Polygon"
#    },
#    "anchor":{
#       "coordinates":[
#          9.950693,
#          57.05804500000001
#       ],
#       "type":"Point"
#    },
#    "aliases":[
      
#    ],
#    "categories":[
      
#    ],
#    "status":3,
#    "baseTypeProperties":{
#       "administrativeid":"9d2a470e-f439-44cf-aada-a0d8acb0c699",
#       "capacity":"0"
#    },
#    "properties":{
#       "name@en":"outsideEnglishName",
#       "tempProperty@en":"",
#       "helloworld": "hellorob",
#       "name@da":"outsideDanishName",
#       "tempProperty@da":"NotEmpty"
#    }
# }

# example = {
#     "id": "b055acde9e4143dd95589de0",
#     "parentId": "e4c730c483e44820b54a4e77",
#     "datasetId": "328dd35ea5aa40748a34341f",
#     "externalId": "B215",
#     "baseType": "room",
#     "displayTypeId": "15d7cbdd8b3d4a299dec9d62",
#     "geometry": {
#       "coordinates": [
#         [
#           [
#             9.9580254,
#             57.0861123
#           ],
#           [
#             9.957967,
#             57.086143
#           ],
#           [
#             9.9579261,
#             57.0861201
#           ],
#           [
#             9.9579845,
#             57.0860893
#           ],
#           [
#             9.9580254,
#             57.0861123
#           ]
#         ]
#       ],
#       "bbox": [
#         9.9579261,
#         57.0860893,
#         9.9580254,
#         57.086143
#       ],
#       "type": "Polygon"
#     },
#     "anchor": {
#       "coordinates": [
#         9.9579757,
#         57.0861162
#       ],
#       "type": "Point"
#     },
#     "aliases": [],
#     "categories": [
#       "e89e3a2a9ba94f22a998e426"
#     ],
#     "status": 3,
#     "baseTypeProperties": {
#       "administrativeid": "2444C6BC-713F-41F4-A4FE-A85CDB413EE4",
#       "class": "Room",
#       "capacity": "0"
#     },
#     "properties": {
#       "name@en": "B215",
#       "name@da": "B215"
#     }
#   }


# geo = GeoData(example)

# print(geo.__dict__)
# print()
# print(geo.properties.name.en)
# print()
# print(geo.status)
# print()
# print(geo.geometry.__dict__)
# print()
# print(geo.anchor.coordinates)
# print(geo.geometry.type)
# print()
# print(geo.baseTypeProperties.Class)
