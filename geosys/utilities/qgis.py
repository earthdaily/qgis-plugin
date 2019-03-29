# coding=utf-8
"""Helpers for QGIS related functionality."""

from qgis.core import Qgis

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


def qgis_version_detailed():
    """Get the detailed version of QGIS.

    :returns: List containing major, minor and patch.
    :rtype: list
    """
    version = str(Qgis.QGIS_VERSION_INT)
    return [int(version[0]), int(version[1:3]), int(version[3:])]


def qgis_version():
    """Get the version of QGIS.

    :returns: QGIS Version where 10700 represents QGIS 1.7 etc.
    :rtype: int
    """
    version = str(Qgis.QGIS_VERSION_INT)
    version = int(version)
    return version
