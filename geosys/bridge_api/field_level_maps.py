# coding=utf-8
"""Implementation of Bridge API field-level-maps endpoint.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import BRIDGE_URLS
from geosys.bridge_api.definitions import COLOR_COMPOSITION
from geosys.bridge_api.utilities import get_definition

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class FieldLevelMapsAPIClient(ApiClient):
    """Field Level Maps API Client

    Managing field-level-maps request to geosys bridge server.

    """
    VERSION = 4

    def __init__(self, access_token, endpoint_url=BRIDGE_URLS['na']['prod']):
        """Implementation of field-level-maps API client.

        This API call requires access_token from identity server.

        :param access_token: The access token.
        :type access_token: str

        :param endpoint_url: The API base url.
        :type endpoint_url: str
        """
        super(FieldLevelMapsAPIClient, self).__init__(
                access_token, endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/field-level-maps/v%s/' % (self.endpoint_url, self.VERSION)

    def get_coverage(self, data, filters=None):
        """Get coverage based on given parameters.

        :param data: Data passed to the API to get specific coverage.
            example: {
                "Geometry": "POLYGON((
                                -86.86701653386694 41.331532756357426,
                                -86.86263916875464 41.331532756357426,
                                -86.86263916875464 41.32450729144166,
                                -86.86701653386694 41.32450729144166,
                                -86.86701653386694 41.331532756357426))",
                "Crop": {
                    "Id": "CORN"
                },
                "SowingDate": "2018-04-15"
            }
        :type data: dict

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
        filters = filters if filters else {}
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        response = self.post(
            self.full_url('coverage'),
            headers=headers,
            params=filters,
            json=data)

        return response.json()

    def get_field_map(self, map_type_key, data, params=None):
        """Get requested field map.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param params: Map creation parameters.
        :type params: dict

        :param data: Map creation data.
            example: {
                "SeasonField": {
                    "Id": "string"
                },
                "Image": {
                    "Date": "string"
                }
            }
        :type data: dict

        :return: JSON response.
            Map data specification based on given parameters.
        :rtype: dict
        """
        params = params if params else {}
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        map_type = get_definition(map_type_key)
        if map_type:
            map_type == COLOR_COMPOSITION and params.update({
                'mapType': COLOR_COMPOSITION['name']
            })
            map_family = map_type['map_family']
            response = self.post(
                self.full_url(
                    'maps', map_family['endpoint'], map_type['name']),
                headers=headers,
                params=params,
                json=data)

            return response.json()

        return {}
