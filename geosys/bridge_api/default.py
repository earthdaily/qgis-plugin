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
        'test': 'https://identity.preprod.geosys-na.com',
        'prod': 'https://identity.geosys-eu.com'
    }
}
BRIDGE_URLS = {
    'na': {
        'test': 'http://api-pp.geosys-na.net',
        'prod': 'http://api.geosys-na.net'
    },
    'eu': {
        'test': 'https://api-pp.geosys-na.net',
        'prod': 'https://api.geosys-eu.net'
    }
}

CLIENT_ID = 'mapproduct_api'
CLIENT_SECRET = 'mapproduct_api.secret'
GRANT_TYPE = 'password'
SCOPE = 'openid offline_access'
MAX_FEATURE_NUMBERS = 10
DEFAULT_N_PLANNED = 0.01

# Default parameters for map creation
DEFAULT_AVE_YIELD = 0.0
DEFAULT_MIN_YIELD = 0.0
DEFAULT_MAX_YIELD = 0.0
DEFAULT_ORGANIC_AVE = 0.0
DEFAULT_ZONE_COUNT = 0.0
DEFAULT_GAIN = 0.0
DEFAULT_OFFSET = 0.0

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
SAMZ_ZONING = 'zoning'
HOTSPOT = 'hotspot'
POSITION = 'position'
FILTER = 'filter'
ZONING_SEGMENTATION = 'zoningSegmentation'
GAIN = 'gain'
OFFSET = 'offset'

# map output format based on Bridge API

# file extension
PGW_EXT = '.pgw'
PNG_KMZ_EXT = '.png.kmz'
PNG_EXT = '.png'
TIFF_EXT = '.tif'
SHP_EXT = '.shp'
KMZ_EXT = '.kmz'
LEGEND_EXT = '.legend.png'

# API key
PNG_KMZ_KEY = 'image:application/vnd.google-earth.kmz+png'
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
PNG_KMZ = {
    'api_key': PNG_KMZ_KEY,
    'extension': PNG_KMZ_EXT
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
LEGEND = {
    'api_key': LEGEND_KEY,
    'extension': LEGEND_EXT
}

ZIPPED_FORMAT = [ZIPPED_TIFF, ZIPPED_SHP]
RASTER_FORMAT = [ZIPPED_TIFF, PNG, PNG_KMZ]
VECTOR_FORMAT = [ZIPPED_SHP, KMZ]
VALID_QGIS_FORMAT = [ZIPPED_TIFF, ZIPPED_SHP, KMZ, PNG, PNG_KMZ]
