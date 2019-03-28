# -*- coding: utf-8 -*-
"""QGIS Settings wrapper.
"""
from qgis.PyQt.QtCore import QSettings
from qgis.core import QgsNetworkAccessManager

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class QGISSettings(object):

    @classmethod
    def get_settings(cls):
        return QSettings()

    @classmethod
    def get_default_tile_expiry(cls, def_value=24):
        return QGISSettings.get_settings().value(
            '/qgis/defaultTileExpiry', def_value, type=int)

    @classmethod
    def set_default_tile_expiry(cls, int_value):
        if not isinstance(int_value, int) or int_value < 0 or (
                int_value > 100000000):
            raise ValueError(int_value)
        return QGISSettings.get_settings().setValue(
            '/qgis/defaultTileExpiry', int_value)

    @classmethod
    def get_default_user_agent(cls, def_value='Mozilla/5.0'):
        return QGISSettings.get_settings().value(
            '/qgis/networkAndProxy/userAgent', def_value, type=str)

    @classmethod
    def set_default_user_agent(cls, str_value):
        if not str_value:
            raise ValueError(str_value)
        return QGISSettings.get_settings().setValue(
            '/qgis/networkAndProxy/userAgent', str_value)

    @classmethod
    def get_default_network_timeout(cls, def_value=60000):
        return QGISSettings.get_settings().value(
            '/qgis/networkAndProxy/networkTimeout', def_value, type=int)

    @classmethod
    def set_default_network_timeout(cls, int_value):
        if not isinstance(int_value, int) or int_value < 1 or (
                int_value > 100000000):
            raise ValueError(int_value)
        return QGISSettings.get_settings().setValue(
            '/qgis/networkAndProxy/networkTimeout', int_value)

    @classmethod
    def get_qgis_proxy(cls):
        s = cls.get_settings()
        proxy_enabled = s.value("proxy/proxyEnabled", u"", type=unicode)
        proxy_type = s.value("proxy/proxyType", u"", type=unicode)
        proxy_host = s.value("proxy/proxyHost", u"", type=unicode)
        proxy_port = s.value("proxy/proxyPort", u"", type=unicode)
        proxy_user = s.value("proxy/proxyUser", u"", type=unicode)
        proxy_password = s.value("proxy/proxyPassword", u"", type=unicode)

        proxy_types = [
            "DefaultProxy", "Socks5Proxy", "HttpProxy", "HttpCachingProxy"
        ]

        if proxy_enabled == "true":
            if proxy_type == "DefaultProxy":
                network_manager = QgsNetworkAccessManager.instance()
                proxy = network_manager.proxy().applicationProxy()
                proxy_host = proxy.hostName()
                proxy_port = str(proxy.port())
                proxy_user = proxy.user()
                proxy_password = proxy.password()

            if proxy_type in proxy_types:
                return proxy_host, proxy_port, proxy_user, proxy_password

        return "", "", "", ""
