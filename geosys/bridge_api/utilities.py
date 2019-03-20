# coding=utf-8
"""This module contains utilities used by Bridge API Interface.
"""
from geosys.bridge_api import definitions

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


def get_definition(keyword, key=None):
    """Given a keyword and a key (optional), try to get a definition
    dict for it.

    :param keyword: A keyword key.
    :type keyword: str

    :param key: A specific key for a deeper search
    :type key: str

    :returns: A dictionary containing the matched key definition
        from definitions, otherwise None if no match was found.
    :rtype: dict, None
    """

    for item in dir(definitions):
        if not item.startswith("__"):
            var = getattr(definitions, item)
            if isinstance(var, dict):
                if var.get('key') == keyword or var.get(key) == keyword:
                    return var
    return None
