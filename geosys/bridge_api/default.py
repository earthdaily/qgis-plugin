# coding=utf-8
"""This module contains default values used by Bridge API Interface.
"""

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

DEFAULT_API_VER = 1

REGION_NA = {
    'key': 'na',
    'description': (
        'US Platform - Fields located in USA, Canada, and Australia.')
}
REGION_EU = {
    'key': 'eu',
    'description': (
        'Fields located in European Platform - Europe, South America and '
        'South Africa.')
}
ALL_REGIONS = [REGION_NA, REGION_EU]

IDENTITY_URLS = {
    'na': {
        'test': 'https://identity.preprod.geosys-na.com',
        'prod': 'https://identity.geosys-na.com'
    },
    'eu': {
        'test': 'https://identity.preprod.geosys-eu.com',
        'prod': 'https://identity.geosys-eu.com'
    }
}
BRIDGE_URLS = {
    'na': {
        'test': 'https://bridge.preprod.geosys-na.com',
        'prod': 'https://bridge.geosys-na.com'
    },
    'eu': {
        'test': 'https://bridge.preprod.geosys-eu.com',
        'prod': 'https://bridge.geosys-eu.com'
    }
}

CLIENT_ID = 'mapproduct_api'
CLIENT_SECRET = 'mapproduct_api.secret'
GRANT_TYPE = 'password'
SCOPE = 'openid offline_access'
MAX_FEATURE_NUMBERS = 10
DEFAULT_ZONE_COUNT = 5

# coverage filters

COVERAGE_TYPE = 'CoverageType'
IMAGE_DATE = 'Image.Date'
IMAGE_SENSOR = 'Image.Sensor'
IMAGE_SOIL_MATERIAL = 'Image.SoilMaterial'
IMAGE_WEATHER = 'Image.Weather'
MAPS_TYPE = 'Maps.Type'
MAP_LIMIT = '$limit'

# map creation parameters

YIELD_AVERAGE = 'HistoricalYieldAverage'
YIELD_MINIMUM = 'MinYieldGoal'
YIELD_MAXIMUM = 'MaxYieldGoal'
ORGANIC_AVERAGE = 'AverageOrganicMatter'
SAMZ_ZONE = 'zoneCount'

# map output format based on Bridge API

# file extension
PGW_EXT = '.pgw'
PNG_EXT = '.png'
TIFF_EXT = '.tif'
SHP_EXT = '.shp'
KMZ_EXT = '.kmz'

# API key
PNG_KEY = 'image:image/png'
ZIPPED_TIFF_KEY = 'image:image/tiff+zip'
ZIPPED_SHP_KEY = 'image:application/shp+zip'
KMZ_KEY = 'image:application/vnd.google-earth.kmz'
THUMBNAIL_KEY = 'thumbnail'
LEGEND_KEY = 'legend'
WORLD_FILE_KEY = 'worldFile'

PGW = {
    'api_key': WORLD_FILE_KEY,
    'extension': PGW_EXT
}
PNG = {
    'api_key': PNG_KEY,
    'extension': PNG_EXT
}
ZIPPED_TIFF = {
    'api_key': ZIPPED_TIFF_KEY,
    'extension': TIFF_EXT
}
ZIPPED_SHP = {
    'api_key': ZIPPED_SHP_KEY,
    'extension': SHP_EXT
}
KMZ = {
    'api_key': KMZ_KEY,
    'extension': KMZ_EXT
}

ZIPPED_FORMAT = [ZIPPED_TIFF, ZIPPED_SHP]
RASTER_FORMAT = [ZIPPED_TIFF, PNG]
VECTOR_FORMAT = [ZIPPED_SHP, KMZ]
VALID_QGIS_FORMAT = [ZIPPED_TIFF, ZIPPED_SHP, KMZ, PNG]
