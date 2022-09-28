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
            'SUNFLOWER', 'PEANUT', 'SOYBEANS', 'ORANGE', 'RICE', 'SORGHUM',
            'WINTER_DURUM_WHEAT', 'WINTER_SOFT_WHEAT', 'SPRING_DURUM_WHEAT',
            'SOFT_WHITE_SPRING_WHEAT', 'TRITICALE', 'WINTER_BARLEY', 'SPRING_BARLEY', 'WINTER_OSR'
        ]
        self.assertEqual(sorted(crops), sorted(expected_crops))

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
        map_type_key = 'INSEASON_NDVI'
        season_field_id = 'bg5bgq3'
        image_date = '2021-11-30'

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

    def test_get_difference_map(self):
        """Test we can successfully get the difference map."""
        map_type_key = 'INSEASON_NDVI'
        season_field_id = 'bg5bgq3'
        earliest_image_date = '2021-09-18'
        latest_image_date = '2021-11-30'

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='mapproduct_api',
            client_secret='mapproduct_api.secret',
            use_testing_service=True)
        field_map = bridge_api.get_difference_map(
            map_type_key, season_field_id,
            earliest_image_date, latest_image_date
        )
        self.assertTrue('seasonField' in field_map)

    def test_get_samz_map(self):
        """Test we can successfully get the SAMZ map."""
        season_field_id = 'lqlv9nb'
        params = {'zoneCount': 5}

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='mapproduct_api',
            client_secret='mapproduct_api.secret',
            use_testing_service=True)

        # test SAMZ auto
        field_map = bridge_api.get_samz_map(
            season_field_id, params=params)
        self.assertTrue('seasonField' in field_map)

        # test SAMZ custom
        list_of_image_date = ['2018-10-13', '2018-10-18']
        field_map = bridge_api.get_samz_map(
            season_field_id, list_of_image_date, params=params)
        self.assertTrue('seasonField' in field_map)

    def test_get_content(self):
        """Test we can successfully get the content of png response."""
        image_id = 'IKc73hpUQ6t1tqdBqbWqEsD4IMwNnwN2zsF6EO4BM2e'
        season_field = 'lqlv9nb'

        thumbnail_url = (
            f"https://api-pp.geosys-na.net:443/field-level-maps/v4/"
            f"season-fields/{season_field}/coverage/{image_id}"
            "/base-reference-map/INSEASONPARTIAL_NDVI/thumbnail.png"
        )

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='mapproduct_api',
            client_secret='mapproduct_api.secret',
            use_testing_service=True)

        content = bridge_api.get_content(thumbnail_url)

        self.assertTrue(isinstance(content, bytes))


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIWrapperTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
