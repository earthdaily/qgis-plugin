# coding=utf-8
"""Implementation of Bridge API field-level-maps endpoint.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import BRIDGE_URLS

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class FieldLevelMapsAPIClientV4(ApiClient):
    """Field Level Maps API Client

    Managing field-level-maps request to geosys identity server.

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
        super(FieldLevelMapsAPIClientV4, self).__init__(
                access_token, endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/field-level-maps/v%s/' % (self.endpoint_url, self.VERSION)

    def get_coverage(self, data, filters):
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

        :return: JSON response
        :rtype: dict
        """
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
