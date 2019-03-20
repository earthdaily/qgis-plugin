# coding=utf-8
"""Implementation of Bridge API notifications endpoint.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import BRIDGE_URLS

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class NotificationsAPIClientV1(ApiClient):
    """Notifications API Client

    Managing notifications request to geosys bridge server.

    """
    VERSION = 1

    def __init__(
            self,
            access_token,
            endpoint_url=BRIDGE_URLS['na']['prod']):
        """Implementation of notifications API client.

        This API call requires access_token from identity server.

        :param access_token: The access token.
        :type access_token: str

        :param endpoint_url: The API base url.
        :type endpoint_url: str
        """
        super(NotificationsAPIClientV1, self).__init__(
            access_token, endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/notifications/v%s/' % (self.endpoint_url, self.VERSION)
