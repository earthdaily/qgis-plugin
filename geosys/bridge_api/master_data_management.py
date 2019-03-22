# coding=utf-8
"""Implementation of Bridge API master-data-management endpoint.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import BRIDGE_URLS

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class MasterDataManagementAPIClient(ApiClient):
    """Master Data Management API Client

    Managing master-data-management request to geosys bridge server.

    """
    VERSION = 6

    def __init__(
            self,
            access_token,
            endpoint_url=BRIDGE_URLS['na']['prod']):
        """Implementation of master-data-management API client.

        This API call requires access_token from identity server.

        :param access_token: The access token.
        :type access_token: str

        :param endpoint_url: The API base url.
        :type endpoint_url: str
        """
        super(MasterDataManagementAPIClient, self).__init__(
            access_token, endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/master-data-management/v%s/' % (
            self.endpoint_url, self.VERSION)
