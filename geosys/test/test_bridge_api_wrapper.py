# coding=utf-8
"""Bridge API wrapper client test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import os
import unittest

from geosys.bridge_api_wrapper import BridgeAPI

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class BridgeAPIWrapperTest(unittest.TestCase):
    """Test Bridge API wrapper class works."""

    def setUp(self):
        """Runs before each test."""
        self.username = os.environ.get('BRIDGE_API_USERNAME', None)
        self.password = os.environ.get('BRIDGE_API_PASSWORD', None)

        # we need to set the credentials as environment variables
        message = ('BRIDGE_API_USERNAME and BRIDGE_API_PASSWORD need to be '
                   'defined as environment variables')
        self.assertIsNotNone(self.username, message)
        self.assertIsNotNone(self.password, message)

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_get_coverage(self):
        """Test we can successfully get the coverage."""
        geom = (
            "POLYGON(("
            "-86.86701653386694 41.331532756357426,"
            "-86.86263916875464 41.331532756357426,"
            "-86.86263916875464 41.32450729144166,"
            "-86.86701653386694 41.32450729144166,"
            "-86.86701653386694 41.331532756357426))")

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            debug=True)
        coverages = bridge_api.get_coverage(
            geometry=geom, crop='CORN', sowing_date='2018-04-15')
        self.assertTrue(len(coverages) > 0)


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIWrapperTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
