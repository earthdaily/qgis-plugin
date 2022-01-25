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

    def __init__(self, access_token='', endpoint_url=''):
        """Base class for API client.

        :param access_token: The access token.
        :type access_token: str

        :param endpoint_url: API base url.
        :type endpoint_url: str
        """
        self.access_token = access_token
        self.endpoint_url = endpoint_url
        self.headers = {
            'authorization': 'Bearer %s' % self.access_token
        }
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

            for protocol in ['http', 'https', 'ftp']:
                self.proxy[protocol] = '%s://%s' % (protocol, proxy_url)

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

    def get(self, url, **kwargs):
        """Fetch JSON response from get request to the API.

        :param url: API url.
        :type url: str

        :param kwargs: requests.get parameters
        :type kwargs: dict

        :return: The API response.
        :rtype: response object
        """
        if kwargs.get('headers'):
            kwargs['headers'].update(self.headers)

        response = get(url, proxies=self.proxy, **kwargs)
        return response

    def post(self, url, **kwargs):
        """Fetch JSON response from post request to the API.

        :param url: API url.
        :type url: str

        :param kwargs: requests.post parameters
        :type kwargs: dict

        :return: The API response.
        :rtype: response object
        """
        if kwargs.get('headers'):
            kwargs['headers'].update(self.headers)

        response = post(url, proxies=self.proxy, **kwargs)
        return response

    def get_content(self, url, params=None):
        """Get the response content.

        :param url: API url.
        :type url: str

        :param params: Request parameters.
        :type params: str

        :return: Response content.
        :rtype: bytes
        """
        response = get(
            url, headers=self.headers, params=params, proxies=self.proxy,
            stream=True)
        return response.content
