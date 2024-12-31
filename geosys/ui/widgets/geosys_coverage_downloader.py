# coding=utf-8
"""Implementation of custom GEOSYS coverage downloader.
"""
import os
import sys
import tempfile
import uuid

from PyQt5.QtCore import QThread, pyqtSignal, QByteArray, QSettings, QDate
from urllib3 import request

from geosys.bridge_api.default import (
    MAPS_TYPE,
    IMAGE_SENSOR,
    IMAGE_DATE,
    COVERAGE_PERCENT,
    DEFAULT_COVERAGE_PERCENT,
    MASK,
    ZIPPED_FORMAT,
    PNG,
    PNG_KMZ,
    KMZ,
    KML,
    PGW,
    PGW2,
    LEGEND,
    SHP_EXT,
    BRIDGE_URLS,
    COLOR_COMPOSITION_THUMBNAIL_URL,
    NDVI_THUMBNAIL_URL,
    NITROGEN_THUMBNAIL_URL,
    S2REP_THUMBNAIL_URL,
    CVIN_THUMBNAIL_URL,
    YGM_THUMBNAIL_URL,
    YPM_THUMBNAIL_URL,
    SAMZ_THUMBNAIL_URL,
    SAMPLEMAP_THUMBNAIL_URL,
    HOTSPOT_URL,
    VEGETATION_ENDPOINT,
    ELEVATION_ENDPOINT,
    SAMZ_ENDPOINT,
    EVI_THUMBNAIL_URL,
    CVI_THUMBNAIL_URL,
    NDMI_THUMBNAIL_URL,
    NDWI_THUMBNAIL_URL,
    GNDVI_THUMBNAIL_URL,
    OM_THUMBNAIL_URL,
    SLOPE_THUMBNAIL_URL, LAI_THUMBNAIL_URL)
from geosys.bridge_api.definitions import (
    SAMZ,
    ELEVATION,
    EVI,
    LAI,
    COLOR_COMPOSITION,
    S2REP,
    REFLECTANCE,
    NDVI,
    SOIL,
    INSEASONFIELD_AVERAGE_NDVI,
    INSEASONFIELD_AVERAGE_LAI,
    INSEASONFIELD_AVERAGE_REVERSE_NDVI,
    INSEASONFIELD_AVERAGE_REVERSE_LAI,
    CVIN,
    OM,
    YGM,
    YVM,
    SAMPLE_MAP, CVI, NDMI, NDWI, GNDVI, SLOPE
)
from geosys.bridge_api_wrapper import BridgeAPI
from geosys.utilities.downloader import fetch_data, extract_zip
from geosys.utilities.qgis_settings import QGISSettings
from geosys.utilities.settings import setting
from geosys.utilities.gui_utilities import create_hotspot_layer
from geosys.utilities.utilities import check_if_file_exists, clean_filename, log
from geosys.bridge_api.utilities import get_definition

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

settings = QSettings()


class CoverageSearchThread(QThread):
    """Thread object wrapper for coverage search."""

    search_started = pyqtSignal()
    search_finished = pyqtSignal()
    data_downloaded = pyqtSignal(object, QByteArray)
    error_occurred = pyqtSignal(object)

    def __init__(
            self,
            geometries,
            crop_type,
            sowing_date,
            map_product,
            sensor_type,
            mask_type,
            start_date,
            end_date,
            geometries_points,
            attributes_points,
            attribute_field,
            mutex,
            coverage_percent,
            n_planned_value=1.0,
            parent=None):
        """Thread object wrapper for coverage search.

        :param geometries: List of geometry filter in WKT format.
        :type geometries: list

        :param crop_type: Crop type.
        :type crop_type: str

        :param sowing_date: Sowing date. yyyy-MM-dd
        :type sowing_date: str

        :param map_product: Map product type.
        :type map_product: str

        :param sensor_type: Sensor type.
        :type sensor_type: str

        :param start_date: Start date of date range. yyyy-MM-dd
        :type start_date: str

        :param end_date: End date of date range. yyyy-MM-dd
        :type end_date: str

        :param mutex: Access serializer.
        :type mutex: QMutex

        :param n_planned_value: Value used by the nitrogen map requests
        :type n_planned_value: Numeric

        :param parent: Parent class.
        :type parent: QWidget
        """
        super(CoverageSearchThread, self).__init__(parent)
        self.geometries = geometries
        self.crop_type = crop_type
        self.sowing_date = sowing_date
        self.map_product = map_product
        self.sensor_type = sensor_type
        self.mask_type = mask_type
        self.start_date = start_date
        self.end_date = end_date
        self.geometries_points = geometries_points
        self.attributes_points = attributes_points
        self.attribute_field = attribute_field
        self.mutex = mutex
        self.coverage_percent = coverage_percent if coverage_percent is not None else DEFAULT_COVERAGE_PERCENT
        self.n_planned_value = n_planned_value
        self.sample_map_data = None
        self.parent = parent

        # setup coverage search filters
        date_filter = ''
        if self.start_date and self.end_date:
            date_filter = '$between:{}|{}'.format(
                self.start_date, self.end_date)
        elif self.end_date:
            date_filter = '$lte:{}'.format(self.end_date)

        # Set coverage percent filter
        coverage_percent_filter = ''
        if self.coverage_percent:
            coverage_percent_filter = f'$gte:{self.coverage_percent}'
        else:
            # Using this as the min value is captured as None
            coverage_percent_filter = f'$gte:{0}'

        # Disable filter when map product is Elevation
        self.filters = {}
        if self.map_product != ELEVATION['key'] or self.map_product != SLOPE['key']:
            if self.map_product == REFLECTANCE['key']:
                # Catalog-imagery API call. Maps.Type will be set to NDVI
                # This is a work-around provided by GeoSys, because reflectance results
                # are not shown in the response from the API
                if self.mask_type in {'All', 'None'}:
                    self.filters.update({
                        MAPS_TYPE: NDVI['key'],
                        IMAGE_DATE: date_filter,
                        COVERAGE_PERCENT: coverage_percent_filter
                    })
                    self.sensor_type and self.filters.update({
                        IMAGE_SENSOR: self.sensor_type
                    })
                else:
                    # Mask type required
                    self.filters.update({
                        MAPS_TYPE: NDVI['key'],
                        IMAGE_DATE: date_filter,
                        COVERAGE_PERCENT: coverage_percent_filter,
                        MASK: self.mask_type
                    })
                    self.sensor_type and self.filters.update({
                        IMAGE_SENSOR: self.sensor_type
                    })
            elif self.map_product == SOIL['key']:
                # This is a workaround to get the seasonfield ID
                # This has been suggested by GeoSys
                self.filters.update({
                    # This is included for a shorter response
                    MAPS_TYPE: NDVI['key'],
                    IMAGE_DATE: date_filter,
                    COVERAGE_PERCENT: coverage_percent_filter
                })
                self.sensor_type and self.filters.update({
                    IMAGE_SENSOR: self.sensor_type
                })
            elif self.map_product == SAMPLE_MAP['key']:
                if self.mask_type in {'All', 'None'}:
                    self.filters.update({
                        MAPS_TYPE: NDVI['key'],
                        IMAGE_DATE: date_filter,
                        COVERAGE_PERCENT: coverage_percent_filter
                    })
                else:
                    self.filters.update({
                        MAPS_TYPE: NDVI['key'],
                        IMAGE_DATE: date_filter,
                        COVERAGE_PERCENT: coverage_percent_filter,
                        MASK: self.mask_type
                    })
                self.sensor_type and self.filters.update({
                    IMAGE_SENSOR: self.sensor_type
                })
            elif self.map_product == SAMZ['key']:
                if self.mask_type in {'All', 'None'}:
                    self.filters.update({
                        MAPS_TYPE: COLOR_COMPOSITION['key'],
                        IMAGE_DATE: date_filter
                    })
                    self.sensor_type and self.filters.update({
                        IMAGE_SENSOR: self.sensor_type
                    })
                else:
                    self.filters.update({
                        MAPS_TYPE: COLOR_COMPOSITION['key'],
                        IMAGE_DATE: date_filter,
                        MASK: self.mask_type
                    })
                    self.sensor_type and self.filters.update({
                        IMAGE_SENSOR: self.sensor_type
                    })
            else:
                # Coverage API call. Maps.Type should be included
                if self.mask_type in {'All', 'None'}:
                    # Mask not required
                    self.filters.update({
                        MAPS_TYPE: self.map_product,
                        IMAGE_DATE: date_filter,
                        COVERAGE_PERCENT: coverage_percent_filter
                    })
                    self.sensor_type and self.filters.update({
                        IMAGE_SENSOR: self.sensor_type
                    })
                else:
                    # Mask type required
                    self.filters.update({
                        MAPS_TYPE: self.map_product,
                        IMAGE_DATE: date_filter,
                        MASK: self.mask_type,
                        COVERAGE_PERCENT: coverage_percent_filter
                    })
                    self.sensor_type and self.filters.update({
                        IMAGE_SENSOR: self.sensor_type
                    })

        self.settings = QSettings()

        self.need_stop = False

    def run(self):
        """Start thread job."""
        self.search_started.emit()

        results = None

        # search
        try:
            self.mutex.lock()

            searcher_client = BridgeAPI(
                *credentials_parameters_from_settings(),
                proxies=QGISSettings.get_qgis_proxy())

            catalog_imagery_api = [
                S2REP['key'],
                REFLECTANCE['key'],
                CVIN['key'],
                INSEASONFIELD_AVERAGE_NDVI['key'],
                INSEASONFIELD_AVERAGE_LAI['key'],
                INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
                INSEASONFIELD_AVERAGE_REVERSE_LAI['key'],
                YGM['key'],
                YVM['key'],
                SAMZ['key'],
                SAMPLE_MAP['key']
            ]
            collected_results = []
            for geometry in self.geometries:
                results = searcher_client.get_catalog_imagery(
                    geometry, self.crop_type, self.sowing_date,
                    filters=self.filters
                )

                if isinstance(results, dict) and results.get('message'):
                    # TODO handle model_validation_error
                    raise Exception(results['message'])

                sample_map_ids = []
                for result in results:

                    request_data = None
                    result['seasonField']['geometry'] = geometry
                    # Get thumbnail content
                    if self.need_stop:
                        break

                    requested_map = None

                    nitrogen_products = [
                        INSEASONFIELD_AVERAGE_NDVI['key'],
                        INSEASONFIELD_AVERAGE_LAI['key'],
                        INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
                        INSEASONFIELD_AVERAGE_REVERSE_LAI['key']
                    ]

                    if self.map_product == SAMPLE_MAP['key']:
                        # Sample maps has a different workflow than other map products
                        # The sample maps first needs to be created, and then the thumbnails
                        # can be retrieved.

                        # Required parameters for Sample maps
                        image = result['image']
                        image_id = image['id']
                        image_date = image['date']
                        season_field = result['seasonField']
                        result_ids = {
                            'image_id': image_id,
                        }
                        sample_map_ids.append(result_ids)

                        data = []
                        i = 0
                        # Create the request data from the points and its
                        # values
                        for geom in self.geometries_points:
                            val = self.attributes_points[i]
                            data_item = {
                                "geometry": geom,
                                "value": val
                            }
                            data.append(data_item)

                            i += 1
                        # The final request data
                        request_data = {
                            "seasonField": {
                                "Id": None,
                                "geometry": geometry,
                            },
                            "properties": {
                                "nutrientType": self.attribute_field
                            },
                            "data": data
                        }

                        self.sample_map_data = request_data

                        bridge_api = BridgeAPI(
                            *credentials_parameters_from_settings(),
                            proxies=QGISSettings.get_qgis_proxy())

                        # Set directLinks to false for Sample maps to receive direct links
                        # API requires it to be as such
                        params = {
                            'directlinks': 'false',
                            '$epsg-out': '4326'
                        }

                        # Perform the request
                        # This step now "creates" the sample map
                        field_map_json = bridge_api.get_field_map(
                            SAMPLE_MAP['key'],
                            None,
                            image_date,
                            image_id,
                            sample_map_data=request_data,
                            params=params
                        )

                    elif self.map_product in nitrogen_products:
                        # Set the requested_map to the nitrogen product key
                        if self.map_product == INSEASONFIELD_AVERAGE_NDVI['key']:
                            requested_map = INSEASONFIELD_AVERAGE_NDVI
                        elif self.map_product == INSEASONFIELD_AVERAGE_LAI['key']:
                            requested_map = INSEASONFIELD_AVERAGE_LAI
                        elif self.map_product == INSEASONFIELD_AVERAGE_REVERSE_NDVI['key']:
                            requested_map = INSEASONFIELD_AVERAGE_REVERSE_NDVI
                        elif self.map_product == INSEASONFIELD_AVERAGE_REVERSE_LAI['key']:
                            requested_map = INSEASONFIELD_AVERAGE_REVERSE_LAI
                    else:
                        # All other map types
                        for map_result in result['maps']:
                            if self.map_product == REFLECTANCE['key'] or self.map_product == SOIL['key']:
                                # Reflectance map and soil map type will make use of the
                                # NDVI to show coverage results
                                # This is a work-around provided by GeoSys
                                if map_result['type'] == NDVI['key']:
                                    requested_map = map_result
                                    break
                            else:  # Other map types
                                if map_result['type'] == self.map_product or (
                                        self.map_product == ELEVATION['key'] or self.map_product == SLOPE['key']):
                                    requested_map = map_result
                                    break

                    # Workflow differs for Sample maps
                    if not requested_map and self.map_product != SAMPLE_MAP['key']:
                        continue

                    thumbnail_url = None

                    image = result['image']
                    image_id = image['id']

                    data = {
                        "image": {
                            "id": image_id
                        },
                        "seasonField":
                            {
                                "geometry": geometry,
                                "crop": self.crop_type
                        }
                    }

                    if self.map_product in [REFLECTANCE['key'], NDVI['key']]:
                        # Reflectance map type should make use of the NDVI thumbnail
                        # This is a work-around provided by GeoSys
                        thumbnail_url = (
                            NDVI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == EVI['key']:
                        thumbnail_url = (
                            EVI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == CVIN['key']:
                        thumbnail_url = (
                            CVIN_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == CVI['key']:
                        thumbnail_url = (
                            CVI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == S2REP['key']:
                        thumbnail_url = (
                            S2REP_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == NDMI['key']:
                        thumbnail_url = (
                            NDMI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == NDWI['key']:
                        thumbnail_url = (
                            NDWI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == LAI['key']:
                        thumbnail_url = (
                            LAI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == GNDVI['key']:
                        thumbnail_url = (
                            GNDVI_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == SLOPE['key']:
                        thumbnail_url = (
                            SLOPE_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == SOIL['key']:
                        thumbnail_url = (
                            SAMPLEMAP_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server,
                                mapType='SOILMAP'
                            ))
                    elif self.map_product == OM['key']:
                        thumbnail_url = (
                            OM_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            )
                        )
                        data.update({
                            "AverageOrganicMatter": 100
                        })
                    elif self.map_product in nitrogen_products:
                        # Nitrogen map type
                        if self.map_product == INSEASONFIELD_AVERAGE_NDVI['key']:
                            #  AVERAGE NDVI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_NDVI['key']))
                            data.update({
                                "nPlanned": f"{self.n_planned_value}",
                                "nMin": 0.001,
                                "nMax": 120,
                            })

                        elif self.map_product == INSEASONFIELD_AVERAGE_LAI['key']:
                            #  AVERAGE LAI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_LAI['key']))
                            data.update({
                                "nPlanned": f"{self.n_planned_value}",
                                "nMin": 0.001,
                                "nMax": 120,
                            })
                        elif self.map_product == INSEASONFIELD_AVERAGE_REVERSE_NDVI['key']:
                            #  AVERAGE REVERSE NDVI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_REVERSE_NDVI['key']))
                            data.update({
                                "nPlanned": f"{self.n_planned_value}",
                                "nMin": 0.001,
                                "nMax": 120,
                            })
                        elif self.map_product == INSEASONFIELD_AVERAGE_REVERSE_LAI['key']:
                            #  AVERAGE REVERSE LAI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_REVERSE_LAI['key']))
                            data.update({
                                "nPlanned": f"{self.n_planned_value}",
                                "nMin": 0.001,
                                "nMax": 120,
                            })
                    elif self.map_product == YGM['key'] or self.map_product == YVM['key']:
                        if self.map_product == YGM['key']:
                            data.update({
                                "HistoricalYieldAverage": 55,
                                "MaxYieldGoal": 120,
                                "MinYieldGoal": 50,
                            })
                            thumbnail_url = (
                                YGM_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server
                                ))
                        else:
                            data.update({
                                "historicalyieldaverage": 50,
                            })
                            thumbnail_url = (
                                YPM_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server
                                ))
                    elif self.map_product == SAMZ['key']:
                        thumbnail_url = (
                            SAMZ_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    elif self.map_product == SAMPLE_MAP['key']:
                        # Sample maps
                        thumbnail_url = (
                            SAMPLEMAP_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server,
                                mapType="SAMPLEMAP"
                            ))

                        data = request_data

                    elif self.map_product == COLOR_COMPOSITION['key']:
                        # Sample maps
                        thumbnail_url = (
                            COLOR_COMPOSITION_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server
                            ))
                    else:  # All other map types
                        thumbnail_url = None

                    if thumbnail_url:
                        thumbnail_content = searcher_client.get_content(
                            thumbnail_url, params={}, data=data)
                        thumbnail_ba = QByteArray(thumbnail_content)
                    else:

                        thumbnail_ba = bytes('', 'utf-8')

                    collected_results.append({
                        'data': result,
                        'thumbnail': thumbnail_ba
                    })

                    if self.map_product == SAMPLE_MAP['key']:
                        # Only one sample needs to be shown
                        # One set created from the points
                        break

            # Using this trick, rendering each list item will not be delayed
            # by thumbnail request.
            for result in collected_results:
                self.data_downloaded.emit(result['data'], result['thumbnail'])

            self.search_finished.emit()
        except Exception as e:
            error_text = (self.tr(
                "Error of processing!\n{0}: {1}")).format(
                unicode(sys.exc_info()[0].__name__), unicode(
                    sys.exc_info()[1]))

            error_text = f"{error_text},-- {e}"
            self.error_occurred.emit(error_text)
        finally:
            self.mutex.unlock()

    def stop(self):
        """Stop thread job."""
        self.need_stop = True


def fetch_map(
        map_specification,
        map_product,
        geometry,
        n_planned_value,
        yield_val,
        min_yield_val,
        max_yield_val,
        data=None,
        params=None,
        crop_type=None,
        gain=None,
        offset=None,
        zone_count=None
):
    """
    Fetch and generate a map based on the given parameters.

    :param map_specification: Coverage image details.
    :type map_specification: dict

    :param map_product: Type of map product to generate (e.g, NDVI).
    :type map_product: str

    :param geometry: Spatial geometry defining
    the area of interest in Well-Known text.
    :type geometry: str

    :param n_planned_value: Planned value used for nitrogen map type.
    :type n_planned_value: int

    :param yield_val: Yield value for crop analysis.
    :type yield_val: int

    :param min_yield_val: Minimum yield value for analysis.
    :type min_yield_val: int

    :param max_yield_val: Maximum yield value for analysis.
    :type max_yield_val: int

    :param data: Optional additional data for map generation.
    :type data: dict, optional

    :param params: Additional parameters for map customization.
    :type params: dict, optional

    :param crop_type: Type of crop to analyze (e.g., WHEAT, CORN).
    :type crop_type: str, optional

    :param gain: Gain factor for map computation.
    :type gain: float, optional

    :param offset: Offset value for map computation.
    :type offset: float, optional

    :param zone_count: Number of zones.
    :type zone_count: int, optional

    :return: Response with map details.
    :rtype: dict
    """

    # Construct map creation parameters
    map_specification.update(map_specification['maps'][0])
    map_specification.update(map_specification['seasonField'])
    map_type_key = map_product
    season_field_id = map_specification['seasonField']['id']
    season_field_geom = geometry
    image_date = map_specification['image']['date']
    image_id = map_specification['image']['id']

    nitrogen_maps = [
        INSEASONFIELD_AVERAGE_NDVI['key'],
        INSEASONFIELD_AVERAGE_LAI['key'],
        INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
        INSEASONFIELD_AVERAGE_REVERSE_LAI['key']
    ]
    if map_type_key == OM['key']:
        request_data = {
            'Image': {
                "Id": image_id
            },
            "AverageOrganicMatter": 100,
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom
            }
        }
    elif map_type_key in nitrogen_maps:
        request_data = {
            'Image': {
                "Id": image_id
            },
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom,
                'crop': crop_type
            },
            "nPlanned": n_planned_value,
            "gain": gain or 1,
            "offset": offset or 0
        }

    elif map_type_key == LAI['key']:
        request_data = {
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom,
                'crop': crop_type
            },
            'Image': {
                'Id': image_id
            }
        }
    else:
        request_data = {
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom
            },
            'Image': {
                'Id': image_id
            },
            "zoneCount": zone_count
        }
    params = params if params else {}
    if data:
        data.update(params or {})
        data.update(request_data)

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())

    if map_type_key == SAMPLE_MAP['key']:

        map_params = {
            'directlinks': 'true',
            '$epsg-out': '4326'
        }
        map_data = {}
        map_data['seasonField'] = data.get('seasonField')
        map_data['properties'] = data.get('properties')
        map_data['data'] = data.get('data')

        # Perform the request
        # This step now "creates" the sample map
        field_map_json = bridge_api.get_field_map(
            SAMPLE_MAP['key'],
            None,
            image_date,
            image_id,
            sample_map_data=map_data,
            params=map_params
        )

        data['request_data'] = map_data
    else:
        field_map_json = bridge_api.get_field_map(
            map_type_key,
            season_field_id,
            season_field_geom,
            image_date,
            image_id,
            n_planned_value,
            yield_val,
            min_yield_val,
            max_yield_val,
            sample_map_id=None,
            zone_count=zone_count,
            **data)

    return field_map_json


def create_map(
        map_specification,
        map_product,
        geometry,
        output_dir,
        filename,
        output_map_format,
        n_planned_value,
        yield_val,
        min_yield_val,
        max_yield_val,
        sample_map_id=None,
        data=None,
        params=None,
        crop_type=None,
        gain=None,
        offset=None,
        zone_count=None
):
    """Create map based on given parameters.

    :param map_specification: Result of single map coverage specifications.
        example: {
            "seasonField": {
                "id": "zgzmbrm",
                "customerExternalId": "..."
            },
            "image": {
                "date": "2018-10-18",
                "sensor": "SENTINEL_2",
                "soilMaterial": "BARE"
            }
            "type": "NDVI",
            "_links": {
                "self": "the_url",
                "worldFile": "the_url",
                "thumbnail": "the_url",
                "legend": "the_url",
                "image:image/png": "the_url",
                "image:image/tiff+zip": "the_url",
                "image:application/shp+zip": "the_url",
                "image:application/vnd.google-earth.kmz": "the_url"
            },
            "coverageType": "CLEAR"
        }
    :type map_specification: dict

    :param output_dir: Base directory of the output.
    :type output_dir: str

    :param filename: Filename of the output.
    :type filename: str

    :param output_map_format: Output map format.
    :type output_map_format: dict

    :param n_planned_value: Value used for nitrogen map type
    :type n_planned_value: int

    :param yield_val: Yield value
    :type yield_val: int

    :param min_yield_val: Minimum yield value
    :type min_yield_val: int

    :param max_yield_val: Maximum yield value
    :type max_yield_val: int

    :param data: Map creation data.
        example: {
            "MinYieldGoal": 0,
            "MaxYieldGoal": 0,
            "HistoricalYieldAverage": 0
        }
    :type data: dict

    :param sample_map_id: Sample map ID received from the API
    :type sample_map_id: str

    :param params: Map creation parameters.
    :type params: dict
    """""
    # Construct map creation parameters
    map_specification.update(map_specification['maps'][0])
    map_specification.update(map_specification['seasonField'])
    map_type_key = map_product
    season_field_id = map_specification['seasonField']['id']
    season_field_geom = geometry
    image_date = map_specification['image']['date']
    image_id = map_specification['image']['id']
    filename = clean_filename(filename)
    destination_base_path = os.path.join(output_dir, filename)
    nitrogen_maps = [
        INSEASONFIELD_AVERAGE_NDVI['key'],
        INSEASONFIELD_AVERAGE_LAI['key'],
        INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
        INSEASONFIELD_AVERAGE_REVERSE_LAI['key']
    ]
    if map_type_key == OM['key']:
        request_data = {
            'Image': {
                "Id": image_id
            },
            "AverageOrganicMatter": 100,
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom
            }
        }
    elif map_type_key in nitrogen_maps:
        request_data = {
            'Image': {
                "Id": image_id
            },
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom,
                'crop': crop_type
            },
            "nPlanned": n_planned_value,
            "gain": gain or 1,
            "offset": offset or 0
        }

    elif map_type_key == LAI['key']:
        request_data = {
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom,
                'crop': crop_type
            },
            'Image': {
                'Id': image_id
            }
        }

    elif map_type_key == SOIL['key']:
        request_data = {
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom,
            }
        }
    else:
        request_data = {
            'SeasonField': {
                'Id': season_field_id,
                'geometry': season_field_geom
            },
            'Image': {
                'Id': image_id
            },
            "zoneCount": zone_count
        }
    params = params if params else {}
    if data:
        data.update(params or {})
        data.update(request_data)

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())

    if map_type_key == SOIL['key']:
        data = request_data

    if map_type_key == SAMPLE_MAP['key']:

        map_params = {
            'directlinks': 'true',
            '$epsg-out': '4326'
        }
        map_data = {}
        map_data['seasonField'] = data.get('seasonField')
        map_data['properties'] = data.get('properties')
        map_data['data'] = data.get('data')

        # Perform the request
        # This step now "creates" the sample map
        field_map_json = bridge_api.get_field_map(
            SAMPLE_MAP['key'],
            None,
            image_date,
            image_id,
            sample_map_data=map_data,
            params=map_params
        )

        data['request_data'] = map_data
    else:
        field_map_json = bridge_api.get_field_map(
            map_type_key,
            season_field_id,
            season_field_geom,
            image_date,
            image_id,
            n_planned_value,
            yield_val,
            min_yield_val,
            max_yield_val,
            sample_map_id=None,
            zone_count=zone_count,
            **data)

    log(f"used data for SOIL {data} \n map json {field_map_json}")

    result, message = download_field_map(
        field_map_json=field_map_json,
        map_type_key=map_type_key,
        destination_base_path=destination_base_path,
        output_map_format=output_map_format,
        headers=bridge_api.headers,
        map_specification=map_specification,
        data=data,
        image_id=image_id, zone_count=zone_count)

    return result, message


def create_difference_map(
        map_specifications,
        output_dir,
        filename,
        output_map_format,
        data=None,
        params=None):
    """Create map based on given parameters.

    :param map_specifications: List of map coverage specification.
        example: [{
            "seasonField": {
                "id": "zgzmbrm",
                "customerExternalId": "..."
            },
            "image": {
                "date": "2018-10-18",
                "sensor": "SENTINEL_2",
                "soilMaterial": "BARE"
            }
            "type": "NDVI",
            "_links": {
                "self": "the_url",
                "worldFile": "the_url",
                "thumbnail": "the_url",
                "legend": "the_url",
                "image:image/png": "the_url",
                "image:image/tiff+zip": "the_url",
                "image:application/shp+zip": "the_url",
                "image:application/vnd.google-earth.kmz": "the_url"
            },
            "coverageType": "CLEAR"
        }, {...}]
    :type map_specifications: list

    :param output_dir: Base directory of the output.
    :type output_dir: str

    :param filename: Filename of the output.
    :type filename: str

    :param output_map_format: Output map format.
    :type output_map_format: dict

    :param data: Map creation data.
        example: {
            "MinYieldGoal": 0,
            "MaxYieldGoal": 0,
            "HistoricalYieldAverage": 0
        }
    :type data: dict

    :param params: Map creation parameters.
    :type params: dict
    """""
    # Difference map only created from 2 map specifications.
    # Map type and season field id should always be the same between two map.
    for map_specification in map_specifications:
        map_specification.update(map_specification['maps'][0])
    map_type_key = map_specifications[0]['type']
    season_field_id = map_specifications[0]['seasonField']['id']
    earliest_image_date = map_specifications[0]['image']['date']
    latest_image_date = map_specifications[1]['image']['date']
    filename = clean_filename(filename)
    destination_base_path = os.path.join(output_dir, filename)
    data = data if data else {}
    params = params if params else {}
    data.update({'params': params})

    # First, make sure latest date is greater than earliest date
    latest_date = QDate.fromString(latest_image_date, 'yyyy-MM-dd')
    earliest_date = QDate.fromString(earliest_image_date, 'yyyy-MM-dd')
    if earliest_date > latest_date:
        latest_image_date = earliest_date.toString('yyyy-MM-dd')
        earliest_image_date = latest_date.toString('yyyy-MM-dd')

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())
    difference_map_json = bridge_api.get_difference_map(
        map_type_key, season_field_id,
        earliest_image_date, latest_image_date, **data)

    return download_field_map(
        field_map_json=difference_map_json,
        map_type_key=map_type_key,
        destination_base_path=destination_base_path,
        output_map_format=output_map_format,
        headers=bridge_api.headers,
        data=data)


def fetch_samz_map(
        geometry,
        list_of_image_ids,
        list_of_image_date,
        zone_count
):
    """Fetch and generate SAMZ map based on the given parameters.

    :param geometry: Spatial geometry defining the area of interest in WKT (Well-Known Text) format.
        Example:
        "POLYGON ((30.5 -10.5, 30.6 -10.6, 30.7 -10.7, 30.5 -10.5))"
    :type geometry: str

    :param list_of_image_ids: List of image IDs to be used in map generation.
        Example:
        ["image_id_1", "image_id_2", "image_id_3"]
    :type list_of_image_ids: list[str]

    :param list_of_image_date: List of corresponding dates for the images in ISO 8601 format.
        Example:
        ["2022-05-01", "2022-05-10", "2022-05-20"]
    :type list_of_image_date: list[str]

    :param zone_count: Number of zones or regions to segment the map into.
        Example: 5
    :type zone_count: int

    :return: SAMZ map dict based on the provided parameters.
    :rtype: dict
    """

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())

    samz_map_json = bridge_api.get_samz_map(
        geometry,
        list_of_image_ids,
        list_of_image_date,
        zone_count=zone_count,
    )

    return samz_map_json


def create_samz_map(
        geometry,
        list_of_image_ids,
        list_of_image_date,
        zone_count,
        output_dir,
        filename,
        output_map_format,
        data=None,
        params=None):
    """Create map based on given parameters.

    :param season_field_id: ID of the season field.
    :param season_field_id: str

    :param list_of_image_ids: List of selected image IDs
    :param list_of_image_ids: list

    :param list_of_image_date: List of image date indicating the maps
        which are going to be compiled.
    :type list_of_image_date: list

    :param output_dir: Base directory of the output.
    :type output_dir: str

    :param filename: Filename of the output.
    :type filename: str

    :param output_map_format: Output map format.
    :type output_map_format: dict

    :param data: Map creation data.
        example: {
            "MinYieldGoal": 0,
            "MaxYieldGoal": 0,
            "HistoricalYieldAverage": 0
        }
    :type data: dict

    :param params: Map creation parameters.
    :type params: dict
    """""
    map_type_key = SAMZ['key']
    filename = clean_filename(filename)
    destination_base_path = os.path.join(output_dir, filename)
    data = data if data else {}
    params = params if params else {}
    data.update({'params': params})

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())
    samz_map_json = bridge_api.get_samz_map(
        geometry,
        list_of_image_ids,
        list_of_image_date,
        zone_count=zone_count,
    )
    # Construct map creation parameters
    request_data = {
        "SeasonField": {
            "Id": None,
            "geometry": geometry
        },
        "Images": [
            {"id": image_id} for image_id in list_of_image_ids
        ],
        "zoneCount": zone_count
    }

    data['request_data'] = request_data
    data.pop('params', None)
    data.update(params)

    return download_field_map(
        field_map_json=samz_map_json,
        map_type_key=map_type_key,
        destination_base_path=destination_base_path,
        output_map_format=output_map_format,
        headers=bridge_api.headers,
        data=data)


def create_rx_map(
        rx_map_json,
        source_map_id,
        zone_count,
        output_dir,
        filename,
        output_map_format,
        data=None,
        patch_data=None,
        params=None):
    """Create map based on given parameters.

    :param rx_map_json: JSON response from Bridge API field map request.
    :type rx_map_json: dict

    :param source_map_id: ID of the season field.
    :param source_map_id: str

    :param output_dir: Base directory of the output.
    :type output_dir: str

    :param filename: Filename of the output.
    :type filename: str

    :param output_map_format: Output map format.
    :type output_map_format: dict

    :param data: Map creation data.
        example: {
            "MinYieldGoal": 0,
            "MaxYieldGoal": 0,
            "HistoricalYieldAverage": 0
        }
    :type data: dict

    :param params: Map creation parameters.
    :type params: dict
    """""
    map_type_key = "rx-map"
    filename = clean_filename(filename)
    destination_base_path = os.path.join(output_dir, filename)
    data = {
        "name": "MyRx MPv5",
        "tags": [
            "RX_MAP"
        ],
        "sourceMapId": source_map_id,
        "zoneCount": zone_count
    }
    params = params if params else {}
    data.update({'params': params})

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())

    patch_rx_map_json = bridge_api.patch_rx_map(
        source_map_id=source_map_id,
        patch_data=patch_data
    )

    rx_map_json_2 = bridge_api.get_rx_generated(
        url=bridge_api.bridge_server,
        source_map_id=source_map_id,
    )

    return download_field_map(
        field_map_json=rx_map_json,
        map_type_key=map_type_key,
        destination_base_path=destination_base_path,
        output_map_format=output_map_format,
        headers=bridge_api.headers,
        data=data)


def download_field_map(
    field_map_json,
    map_type_key,
    destination_base_path,
    output_map_format,
    headers,
    map_specification=None,
    data=None,
    image_id='',
    zone_count=None
):
    """Download field map from requested field map json.

    :param field_map_json: JSON response from Bridge API field map request.
    :type field_map_json: dict

    :param map_type_key: Map type.
    :type map_type_key: str

    :param destination_base_path: The destination base path where the shp
        will be written to.
    :type destination_base_path: str

    :param output_map_format: Output map format.
    :type output_map_format: dict

    :param headers: Extra headers containing Bridge API authorization.
    :type headers: str

    :param map_specification: Result of single map coverage specifications.
        example: {
            "seasonField": {
                "id": "zgzmbrm",
                "customerExternalId": "..."
            },
            "image": {
                "date": "2018-10-18",
                "sensor": "SENTINEL_2",
                "soilMaterial": "BARE"
            }
            "type": "NDVI",
            "_links": {
                "self": "the_url",
                "worldFile": "the_url",
                "thumbnail": "the_url",
                "legend": "the_url",
                "image:image/png": "the_url",
                "image:image/tiff+zip": "the_url",
                "image:application/shp+zip": "the_url",
                "image:application/vnd.google-earth.kmz": "the_url"
            },
            "coverageType": "CLEAR"
        }
    :type map_specification: dict

    :param data: Map creation data
    :type data: dict

    :param image_id: Image ID used for the catalog-image requests
    :type image_id: str
    """
    message = '{} map successfully created.'.format(map_type_key)
    if not field_map_json.get('seasonField'):
        # field map request error
        message = '{} map request failed.'.format(map_type_key)
        if field_map_json.get('message'):
            message = '{} {}'.format(message, field_map_json['message'])
        return False, message
    # If request succeeded, download zipped map and extract it
    # in requested format.
    map_extension = output_map_format['extension']

    request_data = data.get('request_data') if 'request_data' in data else data

    try:
        seasonfield_id = field_map_json['seasonField']['id']
        if map_type_key == "SAMZ":  # Handle SAMZ-specific URL construction
            # Retrieve the bridge server URL
            username, password, region, client_id, client_secret, use_testing_service = credentials_parameters_from_settings()
            bridge_server = (BRIDGE_URLS[region]['test']
                             if use_testing_service
                             else BRIDGE_URLS[region]['prod'])
            if output_map_format in ZIPPED_FORMAT or output_map_format == KML:
                url = (f"{bridge_server}/field-level-maps/v5/maps/management-zones-map/"
                       f"{map_type_key}/image{output_map_format['extension']}")
                method = 'POST'
            else:
                url = field_map_json['_links'][output_map_format['api_key']]
        elif map_type_key == REFLECTANCE['key']:
            # This is only for reflectance map type
            # Also, reflectance can ONLY make use of tiff.zip format

            # Retrieve the bridge server URL
            username, password, region, client_id, client_secret, use_testing_service = credentials_parameters_from_settings()
            bridge_server = (BRIDGE_URLS[region]['test']
                             if use_testing_service
                             else BRIDGE_URLS[region]['prod'])

            reflectance_map_family = REFLECTANCE['map_family']
            url = (f"{bridge_server}/field-level-maps/v5/maps/{reflectance_map_family['endpoint']}/"
                   f"{map_type_key}/image{output_map_format['extension']}")
            method = 'POST'
        elif map_type_key == "rx-map":
            # Special handling for RX maps
            # Retrieve the bridge server URL
            username, password, region, client_id, client_secret, use_testing_service = credentials_parameters_from_settings()
            bridge_server = (BRIDGE_URLS[region]['test']
                             if use_testing_service
                             else BRIDGE_URLS[region]['prod'])
            if output_map_format in ZIPPED_FORMAT or output_map_format == KML:
                source_map_id = field_map_json.get('id')
                url = (f"{bridge_server}/field-level-maps/v5/maps/"
                       f"{source_map_id}/image{output_map_format['extension']}")
                method = 'GET'
            else:
                url = field_map_json['_links'][output_map_format['api_key']]
        else:  # Other map types
            if map_type_key == YGM['key']:
                request_data['HistoricalYieldAverage'] = 55
                request_data['MaxYieldGoal'] = 120
                request_data['MinYieldGoal'] = 50

            map_type = get_definition(map_type_key)
            map_family = map_type['map_family']

            username, password, region, client_id, client_secret, use_testing_service = credentials_parameters_from_settings()
            bridge_server = (BRIDGE_URLS[region]['test']
                             if use_testing_service
                             else BRIDGE_URLS[region]['prod'])
            if output_map_format in ZIPPED_FORMAT or output_map_format == KML:
                url = (f"{bridge_server}/field-level-maps/v5/maps/{map_family['endpoint']}/"
                       f"{map_type_key}/image{output_map_format['extension']}")
                method = 'POST'
            else:
                url = field_map_json['_links'][output_map_format['api_key']]

    except KeyError:
        # requested map format not found
        message = (
            '{} format not found. '
            'Please select another output format.'.format(
                output_map_format['api_key']))
        return False, message

    try:
        if output_map_format in ZIPPED_FORMAT:
            zip_path = tempfile.mktemp('{}.zip'.format(map_extension))
            url = '{}.zip'.format(url)
            if zone_count:
                url = f"{url}?zoning=true&zoneCount={zone_count}"

            fetch_data(
                url,
                zip_path,
                headers=headers,
                method=method,
                payload=request_data)
            extract_zip(zip_path, destination_base_path)
        elif output_map_format == KML:
            destination_filename = (
                destination_base_path + output_map_format['extension'])
            if zone_count:
                url = f"{url}?zoning=true&zoneCount={zone_count}"
            fetch_data(
                url,
                destination_filename,
                headers=headers,
                method=method,
                payload=request_data)
        else:
            destination_filename = (
                destination_base_path + output_map_format['extension'])

            fetch_data(url, destination_filename, headers=headers)
            if output_map_format == PNG or output_map_format == PNG_KMZ:
                # Download associated legend and world-file for geo-referencing
                # the PNG file.

                # This step check if the map type is color composition
                # If that is the case, legend will not be included to the items
                # list as the API does not include a legend for color
                # composition
                if map_type_key == COLOR_COMPOSITION['key']:
                    # Color composition has no legend
                    list_items = [PGW2]
                else:
                    # Other maps
                    list_items = [PGW2, LEGEND]

                for item in list_items:
                    destination_filename = '{}{}'.format(
                        destination_base_path, item['extension'])
                    fetch_data(url, destination_filename, headers=headers)

        # Get hotspots for zones if they have been requested by user.
        bridge_api = BridgeAPI(
            *credentials_parameters_from_settings(),
            proxies=QGISSettings.get_qgis_proxy())

        data.pop('request_data', None)

        if data.get('zoning') and data.get('hotspot'):
            vegetation_map_types = [
                'NDVI',
                'EVI',
                'CVI',
                'CVIN',
                'GNDVI',
                'LAI',
                'NDWI',
                'S2REP']
            topology_types = ['EROSION', 'ELEVATION', 'SLOPE']
            samz_types = ['SAMZ']
            if map_type_key in vegetation_map_types:
                base_url = f"{HOTSPOT_URL}/{VEGETATION_ENDPOINT}"
            elif map_type_key in samz_types:
                base_url = f"{HOTSPOT_URL}/{SAMZ_ENDPOINT}"
            elif map_type_key in topology_types:
                base_url = f"{HOTSPOT_URL}/{ELEVATION_ENDPOINT}"
            else:
                message = (f"Hotspots support not available"
                           f" for {map_type_key} map type ")
                return False, message

            params = {
                'Type': data.get('zoningSegmentation', 'Polygon'),
                'ZonesCount': data.get('zoneCount', 5),
                '$epsg-out': 4326
            }

            if base_url == f"{HOTSPOT_URL}/{VEGETATION_ENDPOINT}":
                params['MapType'] = map_type_key
                params['Position'] = data.get('position', 'Average')

            image_data = request_data.get('Image', {}).get('Id')
            image_id = [image_data]

            if not image_data:
                image_id = [image.get("id")
                            for image in request_data.get('Images', [])
                            ]

            request_body = {
                'geometry': request_data.get(
                    'SeasonField',
                    {}).get('geometry'),
                'image_id': image_id
            }

            map_json = bridge_api.get_hotspot(
                base_url, params=params, data=request_body)
            output_dir = setting('output_directory', expected_type=str)

            if not isinstance(map_json, dict):
                message = (f"Failed to fetch hotspots "
                           f"{map_json.status_code}, {map_json.text}")
                return False, message

            crs_authid = (
                f"EPSG:"
                f"{params.get('$epsg-out', 4326)}"
            )

            if map_json.get('OutputData', {}).get('Hotspots'):
                hotspot_filename = (
                    f"{'HotspotsPerPart' if params['Type'] == 'Polygon' else 'HotspotsPerPolygon'}_"
                    f"{params.get('Position').lower() if params.get('Position') else ''}_"
                    f"{str(request_body.get('image_id')[0])[:4] or ''}_"
                    f"{str(uuid.uuid4())[:4] or ''}")

                hotspot_filename = check_if_file_exists(
                    output_dir, hotspot_filename, SHP_EXT)

                create_hotspot_layer(
                    map_json['OutputData']['Hotspots'],
                    'hotspots',
                    hotspot_filename,
                    crs_authid
                )

            if map_json.get('OutputData', {}).get('Zones'):
                segment_filename = (
                    f"{'SegmentsPerPart' if params['Type'] == 'Polygon' else 'SegmentsPerPolygon'}_"
                    f"{params.get('Position').lower() if params.get('Position') else ''}_"
                    f"{str(request_body.get('image_id')[0])[:4] or ''}_"
                    f"{str(uuid.uuid4())[:4] or ''}")

                segment_filename = check_if_file_exists(
                    output_dir, segment_filename, SHP_EXT)

                create_hotspot_layer(
                    map_json['OutputData']['Zones'],
                    'segments',
                    segment_filename,
                    crs_authid
                )

    except Exception as e:
        message = f"Failed to download file. Error: {str(e)}"
        return False, message
    return True, message


def fetch_field_map(geometry, image_id, data, map_type):
    """Fetch map for a given image and geometry.

    :param bridge_api: Instance of the BridgeAPI.
    :type bridge_api: BridgeAPI

    :param geometry: Geometry in WKT format.
    :type geometry: str

    :param season_field_id: Season field ID.
    :type season_field_id: str

    :param image_id: ID of the image to fetch.
    :type image_id: str

    :return: JSON response containing map details.
    :rtype: dict
    """

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())
    map_json = bridge_api.get_field_map(
        map_type_key=map_type,
        season_field_id=None,
        season_field_geom=geometry,
        image_date=None,  # Optional if already filtered
        image_id=image_id,
        data=data
    )
    return map_json


def credentials_parameters_from_settings():
    """Credentials parameters for Bridge API

    :return: Credentials parameters.
    :rtype: tuple
    """
    # Retrieve user's settings credentials.
    username = setting(
        'bridge_api_username',
        expected_type=str, qsettings=settings)
    password = setting(
        'bridge_api_password',
        expected_type=str, qsettings=settings)
    client_id = setting(
        'bridge_api_client_id',
        expected_type=str, qsettings=settings)
    client_secret = setting(
        'bridge_api_client_secret',
        expected_type=str, qsettings=settings)

    # define geosys region
    is_region_eu = setting(
        'geosys_region_eu',
        expected_type=bool, qsettings=settings)
    region = 'eu' if is_region_eu else 'na'

    # define prod or testing service
    use_testing_service = setting(
        'use_testing_service',
        expected_type=bool, qsettings=settings)

    # RETURNED VALUES ORDER FOLLOWS BRIDGE API WRAPPER CLASS PARAMETERS ORDER
    return (
        username, password, region, client_id, client_secret,
        use_testing_service
    )
