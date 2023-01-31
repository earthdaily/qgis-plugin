# coding=utf-8
"""Implementation of Bridge API field-level-maps endpoint.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.default import BRIDGE_URLS
from geosys.bridge_api.definitions import (
    COLOR_COMPOSITION,
    REFLECTANCE,
    SOIL,
    INSEASONFIELD_AVERAGE_NDVI,
    INSEASONFIELD_AVERAGE_LAI,
    INSEASONFIELD_AVERAGE_REVERSE_NDVI,
    INSEASONFIELD_AVERAGE_REVERSE_LAI,
    INSEASON_S2REP,
    SAMZ,
    YVM,
    YGM
)
from geosys.bridge_api.utilities import get_definition

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class FieldLevelMapsAPIClient(ApiClient):
    """Field Level Maps API Client

    Managing field-level-maps request to geosys bridge server.

    """
    VERSION = 4

    def __init__(self, access_token, endpoint_url=BRIDGE_URLS['na']['prod']):
        """Implementation of field-level-maps API client.

        This API call requires access_token from identity server.

        :param access_token: The access token.
        :type access_token: str

        :param endpoint_url: The API base url.
        :type endpoint_url: str
        """
        super(FieldLevelMapsAPIClient, self).__init__(
                access_token, endpoint_url)

    @property
    def base_url(self):
        """Base url of the API.

        :return: API url.
        :rtype: str
        """
        return '%s/field-level-maps/v%s/' % (self.endpoint_url, self.VERSION)

    def get_coverage(self, data, filters=None):
        """Get coverage based on given parameters.

        :param data: Data passed to the API to get specific coverage.
            example: {
                "Geometry": "POLYGON((
                                -86.86701653386694 41.331532756357426,
                                -86.86263916875464 41.331532756357426,
                                -86.86263916875464 41.32450729144166,
                                -86.86701653386694 41.32450729144166,
                                -86.86701653386694 41.331532756357426))",
                "Crop": {
                    "Id": "CORN"
                },
                "SowingDate": "2018-04-15"
            }
        :type data: dict

        :param filters: Filter coverage results.
            example: {
                "Image.Date": "$gte:2010-01-01",
                "coverageType": "CLEAR"
            }
        :type filters: dict

        :return: JSON response.
            List of maps data specification based on given criteria.
        :rtype: list
        """
        filters = filters if filters else {}
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        response = self.post(
            self.full_url('coverage'),
            headers=headers,
            params=filters,
            json=data)

        return response.json()

    def get_catalog_imagery(self, data, filters=None):
        """Get catalog-imagery based on given parameters.

        :param data: Data passed to the API to get specific coverage.
            example: {
                "Geometry": "POLYGON((
                                -86.86701653386694 41.331532756357426,
                                -86.86263916875464 41.331532756357426,
                                -86.86263916875464 41.32450729144166,
                                -86.86701653386694 41.32450729144166,
                                -86.86701653386694 41.331532756357426))",
                "Crop": {
                    "Id": "CORN"
                },
                "SowingDate": "2018-04-15"
            }
        :type data: dict

        :param filters: Filter coverage results.
            example: {
                "Image.Date": "$gte:2010-01-01",
                "coverageType": "CLEAR"
            }
        :type filters: dict

        :return: JSON response.
            List of maps data specification based on given criteria.
        :rtype: list
        """

        print('field level maps: get catalog imagery')

        filters = filters if filters else {}
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        response = self.post(
            self.full_url('catalog-imagery'),
            headers=headers,
            params=filters,
            json=data)

        print('\n\nRESPONSE: ' + str(response.json()))
        print('\n\n')

        return response.json()

    def get_field_map(
            self,
            map_type_key,
            data,
            n_planned=1.0,
            yield_val=None,
            min_yield_val=None,
            max_yield_val=None,
            params=None
    ):
        """Get requested field map.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param data: Map creation data.
            example: {
                "SeasonField": {
                    "Id": "string"
                },
                "Image": {
                    "Date": "string"
                }
            }
        :type data: dict

        :param n_planned: Value used for nitrogen maps
        :type n_planned: float

        :param yield_val: Average yield
        :type yield_val: float

        :param min_yield_val: Minimum yield
        :type min_yield_val: float

        :param max_yield_val: Maximum yield
        :type max_yield_val: float

        :param params: Map creation parameters.
        :type params: dict

        :return: JSON response.
            Map data specification based on given parameters.
        :rtype: dict
        """
        params = params if params else {}
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        map_type = get_definition(map_type_key)
        if map_type:
            map_type == COLOR_COMPOSITION and params.update({
                'mapType': COLOR_COMPOSITION['name']
            })
            map_family = map_type['map_family']
            nitrogen_maps = [
                INSEASONFIELD_AVERAGE_NDVI['key'],
                INSEASONFIELD_AVERAGE_LAI['key'],
                INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
                INSEASONFIELD_AVERAGE_REVERSE_LAI['key']
            ]

            image_id = data['Image']['Id'] if data.get('Image', None) else None
            seasonfield_id = data['SeasonField']['Id'] if data.get('SeasonField', None) else None

            if (map_type['key'] == REFLECTANCE['key'] or
                    map_type['key'] == INSEASON_S2REP['key']):
                # Reflectance and S2REP maps needs to make use of the catalog-imagery API
                full_url = self.full_url(
                    'season-fields',
                    seasonfield_id,
                    'coverage',
                    image_id,
                    map_family['endpoint'],
                    map_type['key']
                )

                response = self.get(
                    full_url,
                    headers=headers,
                    params=params,
                    json=data
                )
            elif map_type['key'] in nitrogen_maps:
                full_url = self.full_url(
                    'season-fields',
                    seasonfield_id,
                    'coverage',
                    image_id,
                    map_family['endpoint'],
                    map_type['key'],
                    'n-planned',
                    str(n_planned)
                )

                response = self.get(
                    full_url,
                    headers=headers,
                    params=params,
                    json=data
                )
            elif map_type['key'] == YVM['key']:
                full_url = self.full_url(
                    'season-fields',
                    seasonfield_id,
                    'coverage',
                    image_id,
                    map_family['endpoint'],
                    map_type['key'],
                    'historical-yield-average',
                    str(yield_val)
                )

                response = self.get(
                    full_url,
                    headers=headers,
                    params=params,
                    json=data
                )
            elif map_type['key'] == YGM['key']:
                full_url = self.full_url(
                    'season-fields',
                    seasonfield_id,
                    'coverage',
                    image_id,
                    map_family['endpoint'],
                    map_type['key'],
                    'historical-yield-average',
                    str(yield_val),
                    'max-yield-Goal',
                    str(max_yield_val),
                    'min-yield-Goal',
                    str(min_yield_val)
                )

                response = self.get(
                    full_url,
                    headers=headers,
                    params=params,
                    json=data
                )
            elif map_type['key'] == SAMZ['key']:
                full_url = self.full_url(
                    'season-fields',
                    seasonfield_id,
                    'management-zones-map',
                    'SAMZ'
                )

                response = self.get(
                    full_url,
                    headers=headers,
                    params=params,
                    json=data
                )
            elif map_type['key'] == SOIL['key']:
                # Body required by soilmap
                # This is a workaround provided by GeoSys
                data = {
                    "provider": "Shared",
                    "asset": "USA",
                    "seasonField": {
                        "id": seasonfield_id
                    }
                }

                full_url = self.full_url(
                    'maps',
                    map_family['endpoint'],
                    map_type['key']
                )
                response = self.post(
                    full_url,
                    headers=headers,
                    params=params,
                    json=data
                )
            else:
                full_url = self.full_url(
                    'maps',
                    map_family['endpoint'],
                    map_type['name']
                )

                response = self.post(
                     full_url,
                     headers=headers,
                     params=params,
                     json=data
                )

            return response.json()

        return {}

    def get_hotspot(self, url, params=None):
        """ Actual method to get zone hotspots.

        :return: JSON response.
            Map data specification based on given parameters.
        :rtype: dict
        """
        params = params if params else {}
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        response = self.get(
            url,
            headers=headers,
            params=params)

        if response:
            return response.json()

        return {}
