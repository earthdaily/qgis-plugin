# coding=utf-8
"""This module contains default values used by Bridge API Interface.
"""

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

DEFAULT_API_VER = 1
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
