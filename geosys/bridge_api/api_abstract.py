# coding=utf-8
"""Abstract class implementation of Bridge API Interface.
"""
import os

from requests import get, post

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class ApiClient(object):
    """Abstract class for API Client."""

    VERSION = 0

    def __init__(self, endpoint_url=''):
        self.endpoint_url = endpoint_url
        self.proxy = {}

    def set_proxy(self, proxy_host, proxy_port, proxy_user, proxy_password):
        """Set proxy server.

        :param proxy_host:
        :type proxy_host:

        :param proxy_port:
        :type proxy_port:

        :param proxy_user:
        :type proxy_user:

        :param proxy_password:
        :type proxy_password:

        :return:
        :rtype:
        """
        if proxy_host != "":
            proxy_url = proxy_host
            if proxy_port != "":
                proxy_url = "%s:%s" % (proxy_url, proxy_port)
            if proxy_user != "":
                proxy_url = "%s:%s@%s" % (
                    proxy_user,
                    proxy_password,
                    proxy_url
                )

            self.proxy = {
                "http": proxy_url
            }

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return self.endpoint_url

    def full_url(self, *args):
        """Full url of the API endpoint.

        :param args: List of endpoints.
        :return: str
        """
        full_url = self.base_url
        for item in args:
            full_url = os.path.join(full_url, item)
        return full_url

    def get_json(self, url, headers=None, params=None):
        """Fetch JSON response from get request to the API.

        :param url: API url.
        :type url: str

        :param headers: Request headers.
        :type headers: dict

        :param params: Request parameters.
        :type params: dict

        :return: The API response.
        :rtype: dict
        """
        _params = {}
        if params is not None:
            _params.update(params)
            _params.update(self.proxy)

        response = get(url, headers=headers, params=_params)
        return response.json()

    def post_json(self, url, headers=None, params=None, data=None):
        """Fetch JSON response from post request to the API.

        :param url: API url.
        :type url: str

        :param headers: Request headers.
        :type headers: dict

        :param params: Request parameters.
        :type params: dict

        :param data: Request body.
        :type data: dict

        :return: The API response.
        :rtype: dict
        """
        _params = {}
        if params is not None:
            _params.update(params)
            _params.update(self.proxy)

        response = post(
            url, headers=headers, params=_params, data=data)
        return response.json()

    def get_content(self, url, params=None):
        """Get the response content.

        :param url: API url.
        :type url: str

        :param params: Request parameters.
        :type params: str

        :return: Response content.
        :rtype: str
        """
        response = get(url, params=params, stream=True)
        return response.content
