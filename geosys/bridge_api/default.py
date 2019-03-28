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

# coverage filters
COVERAGE_TYPE = 'CoverageType'
IMAGE_DATE = 'Image.Date'
IMAGE_SENSOR = 'Image.Sensor'
IMAGE_SOIL_MATERIAL = 'Image.SoilMaterial'
IMAGE_WEATHER = 'Image.Weather'
MAPS_TYPE = 'Maps.Type'

# map output format
THUMBNAIL = 'thumbnail'
LEGEND = 'legend'
PNG = 'image:image/png'
ZIPPED_TIFF = 'image:image/tiff+zip'
ZIPPED_SHP = 'image:application/shp+zip'
KMZ = 'image:application/vnd.google-earth.kmz'
