# coding=utf-8
"""Bridge API connection test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import unittest
import os

from geosys.bridge_api.connection import ConnectionAPIClient
from geosys.bridge_api.default import IDENTITY_URLS, CLIENT_ID, CLIENT_SECRET

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
        client = ConnectionAPIClient(IDENTITY_URLS['na']['test'])
        username = os.environ.get('BRIDGE_API_USERNAME', None)
        password = os.environ.get('BRIDGE_API_PASSWORD', None)

        # we need to set the credentials as environment variables
        message = ('BRIDGE_API_USERNAME and BRIDGE_API_PASSWORD need to be '
                   'defined as environment variables')
        self.assertIsNotNone(username, message)
        self.assertIsNotNone(password, message)

        response = client.get_access_token(
            username, password, CLIENT_ID, CLIENT_SECRET)
        self.assertTrue('access_token' in response)


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIConnectionTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
