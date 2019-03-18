# coding=utf-8
"""Bridge API connection test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import unittest

from geosys.bridge_api.connection import ConnectionAPIClientV2
from geosys.bridge_api.default import IDENTITY_URLS

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class BridgeAPIConnectionTest(unittest.TestCase):
    """Test Bridge API connection works."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_access_token(self):
        """Test we can successfully get the access token."""
        client = ConnectionAPIClientV2(IDENTITY_URLS['na']['test'])
        response = client.get_access_token('Bridge_US_Demo', 'Welcome12k18')
        self.assertTrue('access_token' in response)


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIConnectionTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
