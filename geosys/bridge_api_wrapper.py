# coding=utf-8
"""Implementation of Bridge API Wrapper.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.connection import ConnectionAPIClient
from geosys.bridge_api.default import IDENTITY_URLS, BRIDGE_URLS, ALL_REGIONS
from geosys.bridge_api.definitions import CROPS
from geosys.bridge_api.field_level_maps import FieldLevelMapsAPIClient
from geosys.bridge_api.utilities import get_definition

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


class BridgeAPI(ApiClient):
    """Wrapper client for bridge api."""

    def __init__(
            self,
            username,
            password,
            region,
            client_id,
            client_secret,
            use_testing_service=False):
        """Wrapper implementation for bridge api.

        :param username: Bridge API username.
        :type username: str

        :param password: Bridge API password.
        :type password: str

        :param region: Region of fields.
        :type region: str

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client Secret
        :type client_secret: str

        :param use_testing_service: Testing service flag.
        :type use_testing_service: bool
        """
        super(BridgeAPI, self).__init__()
        self.username = username
        self.password = password
        self.region = region
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_testing_service = use_testing_service
        self.access_token = None

        # authenticate user
        self.authenticated, self.authentication_message = self.authenticate()

        if self.authenticated:
            super(BridgeAPI, self).__init__(access_token=self.access_token)

    @staticmethod
    def get_crops():
        """Get default crops.

        :return: List of crops available.
        :rtype: list
        """
        return CROPS.values()

    @staticmethod
    def get_regions():
        """Get default regions.

        :return: List of tuple of regions available.
        :rtype: list
        """
        regions = []
        for region in ALL_REGIONS:
            regions.append((region['key'], region['description']))
        return regions

    def authenticate(self):
        """Authenticate user using given credentials.

        :return: Authentication status and message.
        :rtype: tuple
        """
        try:
            identity_server = (IDENTITY_URLS[self.region]['test']
                               if self.use_testing_service
                               else IDENTITY_URLS[self.region]['prod'])
            api_client = ConnectionAPIClient(identity_server)
            response = api_client.get_access_token(
                self.username,
                self.password,
                self.client_id,
                self.client_secret)
            if response.get('access_token'):
                self.access_token = response['access_token']
                message = 'Authentication succeeded.'
                return True, message
            else:
                message = (
                    'Authentication failed. Ensure your username, password, '
                    'client id, and client secret are valid for the selected '
                    'region service.')
                return False, message
        except KeyError:
            message = 'Please enter a correct region (NA or EU)'
            return False, message

    def get_coverage(self, geometry, crop, sowing_date, filters=None):
        """Get fields coverage for given parameters.

        :param geometry: A geometry in WKT format.
        :type geometry: str

        :param crop: Crop type.
        :type crop: str

        :param sowing_date: Sowing date. YYYY-MM-DD
        :type sowing_date: str

        :param filters: Filter coverage results.
            example: {
                "Image.Date": "$gte:2010-01-01",
                "coverageType": "CLEAR"
            }
        :type filters: dict

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
                         if self.use_testing_service
                         else BRIDGE_URLS[self.region]['prod'])
        api_client = FieldLevelMapsAPIClient(self.access_token, bridge_server)
        coverages_json = api_client.get_coverage(request_data, filters=filters)

        return coverages_json

    def get_field_map(
            self, map_type_key, season_field_id, image_date, **kwargs):
        """Get requested field map.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param season_field_id: ID of the season field.
        :param season_field_id: str

        :param image_date: Date of the image. yyyy-MM-dd
        :type image_date: str

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        # Construct map creation parameters
        request_data = {
            'SeasonField': {
                'Id': season_field_id
            },
            'Image': {
                'Date': image_date
            }
        }
        request_data.update(kwargs)

        # Get request parameters
        params = kwargs.get('params')

        bridge_server = (BRIDGE_URLS[self.region]['test']
                         if self.use_testing_service
                         else BRIDGE_URLS[self.region]['prod'])
        api_client = FieldLevelMapsAPIClient(self.access_token, bridge_server)
        field_map_json = api_client.get_field_map(
            map_type_key, request_data, params)

        return field_map_json

    def get_difference_map(
            self, map_type_key, season_field_id,
            earliest_image_date, latest_image_date, **kwargs):
        """Get requested difference map.

        Currently this only support INSEASON_NDVI and INSEASON_EVI map.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param season_field_id: ID of the season field.
        :param season_field_id: str

        :param earliest_image_date: Earliest date of the image. yyyy-MM-dd
        :type earliest_image_date: str

        :param latest_image_date: Latest date of the image. yyyy-MM-dd
        :type latest_image_date: str

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        # Construct map creation parameters
        request_data = {
            "SeasonField": {
                "Id": season_field_id
            },
            "EarliestImage": {
                "Date": earliest_image_date
            },
            "LatestImage": {
                "Date": latest_image_date
            }
        }
        request_data.update(kwargs)

        # Get request parameters
        params = kwargs.get('params')

        map_type_definition = get_definition(map_type_key)
        difference_map_definition = map_type_definition['difference_map']

        bridge_server = (BRIDGE_URLS[self.region]['test']
                         if self.use_testing_service
                         else BRIDGE_URLS[self.region]['prod'])
        api_client = FieldLevelMapsAPIClient(self.access_token, bridge_server)
        field_map_json = api_client.get_field_map(
            difference_map_definition['key'], request_data, params)

        return field_map_json
