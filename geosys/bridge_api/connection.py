# coding=utf-8
"""Implementation of Bridge API connection.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import (
    IDENTITY_URLS,
    GRANT_TYPE,
    SCOPE,
    CLIENT_ID,
    CLIENT_SECRET)

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class ConnectionAPIClientV2(ApiClient):
    """Connection API Client

    Managing connection/authentication to geosys identity server.

    """
    VERSION = 2.1

    def __init__(self, endpoint_url=IDENTITY_URLS['na']['prod']):
        super(ConnectionAPIClientV2, self).__init__(endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/v%s/' % (
            self.endpoint_url, self.VERSION)

    def get_access_token(self, username, password):
        """Retrieve access token from geosys identity server.

        :param username: Username
        :type username: str

        :param password: Password
        :type password: str

        :return: JSON response
        :rtype: dict
        """
        data = {
            'username': username,
            'password': password,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': GRANT_TYPE,
            'scope': SCOPE
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        return self.post_json(
            self.full_url('connect', 'token'), headers=headers, data=data)
