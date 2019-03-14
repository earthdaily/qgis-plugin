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
    VERSION = 0

    def __init__(self, endpoint_url=''):
        self.endpoint_url = endpoint_url
        self.proxy = {}

    def set_proxy(self, proxy_host, proxy_port, proxy_user, proxy_password):
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
        return self.endpoint_url

    def full_url(self, *args):
        full_url = self.base_url
        for item in args:
            full_url = os.path.join(full_url, item)
        return full_url

    def get_json(self, url, headers=None, params=None):
        _params = {}
        if params is not None:
            _params.update(params)
            _params.update(self.proxy)

        response = get(url, headers=headers, params=_params)
        return response.json()

    def post_json(self, url, headers=None, params=None, data=None):
        _params = {}
        if params is not None:
            _params.update(params)
            _params.update(self.proxy)

        response = post(
            url, headers=headers, params=_params, data=data)
        return response.json()

    def get_content(self, url, params=None):
        response = get(url, params=params, stream=True)
        return response.content
