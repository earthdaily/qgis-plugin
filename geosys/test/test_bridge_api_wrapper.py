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

    def test_get_crops(self):
        """Test we can get all available crops from definition"""
        crops = BridgeAPI.get_crops()
        expected_crops = [
            'SUGARCANE', 'CORN', 'MILLET', 'GRAPES', 'OTHERS', 'COTTON',
            'SUNFLOWER', 'PEANUT', 'SOYBEANS', 'ORANGE', 'RICE', 'SORGHUM']
        self.assertEqual(crops, expected_crops)

    def test_get_regions(self):
        """Test we can get all available regions from definition"""
        regions = BridgeAPI.get_regions()
        expected_regions = [
            ('na',
             'US Platform - Fields located in USA, Canada, and Australia.'),
            ('eu',
             'Fields located in European Platform - Europe, South America '
             'and South Africa.')]
        self.assertEqual(regions, expected_regions)

    def test_get_coverage(self):
        """Test we can successfully get the coverage."""
        geom = (
            "POLYGON(("
            "-86.86701653386694 41.331532756357426,"
            "-86.86263916875464 41.331532756357426,"
            "-86.86263916875464 41.32450729144166,"
            "-86.86701653386694 41.32450729144166,"
            "-86.86701653386694 41.331532756357426))")
        crop_type = 'CORN'
        sowing_date = '2018-04-15'

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='mapproduct_api',
            client_secret='mapproduct_api.secret',
            use_testing_service=True)
        coverages = bridge_api.get_coverage(
            geometry=geom, crop=crop_type, sowing_date=sowing_date)
        self.assertTrue(len(coverages) > 0)

    def test_get_field_map(self):
        """Test we can successfully get the field map."""
        map_type_key = 'INSEASONFIELD_AVERAGE_NDVI'
        season_field_id = 'zgzmbrm'
        image_date = '2018-10-13'

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='mapproduct_api',
            client_secret='mapproduct_api.secret',
            use_testing_service=True)
        field_map = bridge_api.get_field_map(
            map_type_key, season_field_id, image_date,
            # map creation parameters
            NPlanned=48,
            NMin=20,
            NMax=70
        )
        self.assertTrue('seasonField' in field_map)

    def test_get_content(self):
        """Test we can successfully get the content of png response."""
        thumbnail_url = (
            'https://bridge.preprod.geosys-na.com/field-level-maps/v4/'
            'season-fields/zgzmbrm/coverage/2018-11-02/base-reference-map/'
            'INSEASONPARTIAL_NDVI/thumbnail.png')

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='mapproduct_api',
            client_secret='mapproduct_api.secret',
            use_testing_service=True)

        content = bridge_api.get_content(thumbnail_url)
        self.assertTrue(isinstance(content, str))


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIWrapperTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
