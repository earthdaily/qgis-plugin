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
    VERSION = 1

    def __init__(self, endpoint_url=BRIDGE_URLS['na']['prod']):
        super(NotificationsAPIClientV1, self).__init__(endpoint_url)

    @property
    def base_url(self):
        return '%s/notifications/v%s/' % (self.endpoint_url, self.VERSION)
