# coding=utf-8
"""Implementation of Bridge API Wrapper.
"""
from geosys.bridge_api.connection import ConnectionAPIClient
from geosys.bridge_api.default import IDENTITY_URLS, BRIDGE_URLS, ALL_REGIONS
from geosys.bridge_api.definitions import CROPS
from geosys.bridge_api.field_level_maps import FieldLevelMapsAPIClient

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class MapProduct(object):
    """Wrapper instance of Bridge API Coverage map product"""

    def __init__(self, map_data):
        """BRIDGE API Coverage map product wrapper class.

        :param map_data: Dictionary of API response from Bridge API Coverage
            call. example: {
                "type": "INSEASON_NDVI",
                "_links": {
                    "self": url_to_product,
                    "worldFile": url_to_product,
                    "thumbnail": url_to_product,
                    "legend": url_to_product,
                    "image:image/png": url_to_product,
                    "image:image/tiff+zip": url_to_product,
                    "image:application/shp+zip": url_to_product,
                    "image:application/vnd.google-earth.kmz": url_to_product,
                }
            }
        :type map_data: dict
        """
        self.map_data = map_data

    def map_type(self):
        """Get the type of the map product.

        :return: Map type (NDVI, INSEASON_NDVI, etc).
        :rtype: str
        """
        return self.map_data.get('type', '')

    def get_output_url(self, output_format):
        """Get the url of map product based on output format.

        :param output_format: Map output format.
        :type output_format: str

        :return: The url of map product.
        :rtype: str
        """
        return self.map_data.get('_links', {}).get(output_format, {})


class BridgeAPI(object):
    """Wrapper client for bridge api."""

    def __init__(self, username, password, region, debug=False):
        """Wrapper implementation for bridge api.

        :param username: Bridge API username.
        :type username: str

        :param password: Bridge API password.
        :type password: str

        :param region: Region of fields.
        :type region: str

        :param debug: Debug mode flag.
        :type debug: bool
        """
        self.username = username
        self.password = password
        self.region = region
        self.debug = debug
        self.access_token = None

        # authenticate user
        success, message = self.authenticate()
        if not success:
            raise Exception(message)

    def authenticate(self):
        """Authenticate user using given credentials.

        :return: Authentication status and message.
        :rtype: tuple
        """
        try:
            identity_server = (IDENTITY_URLS[self.region]['test']
                               if self.debug
                               else IDENTITY_URLS[self.region]['prod'])
            api_client = ConnectionAPIClient(identity_server)
            response = api_client.get_access_token(
                self.username, self.password)
            if response.get('access_token'):
                self.access_token = response['access_token']
                message = 'Authentication complete'
                return True, message
            else:
                message = 'Authentication failed'
                return False, message
        except KeyError:
            message = 'Please enter a correct region (NA or EU)'
            return False, message

    @staticmethod
    def get_crops(self):
        """Get default crops available.

        :return: List of crops available.
        :rtype: list
        """
        return CROPS.values()

    @staticmethod
    def get_regions(self):
        """Get default regions available

        :return: List of tuple of regions available.
        :rtype: list
        """
        regions = []
        for region in ALL_REGIONS:
            regions.append((region['key'], region['description']))
        return regions

    def get_coverage(self, geometry, crop, sowing_date):
        """Get fields coverage for given parameters.

        :param geometry: A geometry in WKT format.
        :type geometry: str

        :param crop: Crop type.
        :type crop: str

        :param sowing_date: Sowing date. YYYY-MM-DD
        :type sowing_date: str

        :return: JSON response.
            List of maps data specification based on given criteria.
        :rtype: list
        """
        # Construct parameter
        request_data = {
            'Geometry': geometry,
            'Crop': {
                'ID': crop
            },
            'SowingDate': sowing_date
        }

        bridge_server = (BRIDGE_URLS[self.region]['test']
                         if self.debug
                         else BRIDGE_URLS[self.region]['prod'])
        api_client = FieldLevelMapsAPIClient(self.access_token, bridge_server)
        coverages_json = api_client.get_coverage(request_data)

        return coverages_json
