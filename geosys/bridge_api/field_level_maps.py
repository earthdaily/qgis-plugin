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
    """Connection API Client

    Managing field-level-maps request to geosys identity server.

    """
    VERSION = 4

    def __init__(self, endpoint_url=BRIDGE_URLS['na']['prod']):
        super(FieldLevelMapsAPIClientV4, self).__init__(endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/field-level-maps/v%s/' % (self.endpoint_url, self.VERSION)
