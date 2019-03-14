# coding=utf-8
"""Implementation of Bridge API master-data-management endpoint.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import BRIDGE_URLS

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class MasterDataManagementAPIClientV6(ApiClient):
    VERSION = 6

    def __init__(self, endpoint_url=BRIDGE_URLS['na']['prod']):
        super(MasterDataManagementAPIClientV6, self).__init__(endpoint_url)

    @property
    def base_url(self):
        return '%s/master-data-management/v%s/' % (
            self.endpoint_url, self.VERSION)
