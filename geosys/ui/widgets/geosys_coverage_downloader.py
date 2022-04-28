# coding=utf-8
"""Implementation of custom GEOSYS coverage downloader.
"""
import os
import sys
import tempfile

from PyQt5.QtCore import QThread, pyqtSignal, QByteArray, QSettings, QDate

from geosys.bridge_api.default import (
    MAPS_TYPE, IMAGE_SENSOR, IMAGE_DATE, ZIPPED_FORMAT, PNG, PNG_CC, PGW, LEGEND, SHP_EXT, BRIDGE_URLS)
from geosys.bridge_api.definitions import (SAMZ,
                                           ELEVATION,
                                           COLOR_COMPOSITION,
                                           INSEASON_S2REP,
                                           REFLECTANCE,
                                           INSEASON_NDVI,
                                           SOIL,
                                           INSEASONFIELD_AVERAGE_NDVI,
                                           INSEASONFIELD_AVERAGE_LAI,
                                           INSEASONFIELD_AVERAGE_REVERSE_NDVI,
                                           INSEASONFIELD_AVERAGE_REVERSE_LAI,
                                           INSEASON_CVIN)
from geosys.bridge_api_wrapper import BridgeAPI
from geosys.utilities.downloader import fetch_data, extract_zip
from geosys.utilities.qgis_settings import QGISSettings
from geosys.utilities.settings import setting
from geosys.utilities.gui_utilities import create_hotspot_layer
from geosys.utilities.utilities import check_if_file_exists

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

settings = QSettings()
NDVI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v4/season-fields/{id}/coverage/{date}'
    '/base-reference-map/INSEASON_NDVI/thumbnail.png')
NITROGEN_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v4/season-fields/{id}/coverage/{image}'
    '/model-map/{nitrogen_map_type}/n-planned/{n_value}/thumbnail.png')
S2REP_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v4/season-fields/{id}/coverage/{image}'
    '/base-reference-map/INSEASON_S2REP/thumbnail.png')
CVIN_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v4/season-fields/{id}/coverage/{image}'
    '/base-reference-map/INSEASON_CVIN/thumbnail.png')



class CoverageSearchThread(QThread):
    """Thread object wrapper for coverage search."""

    search_started = pyqtSignal()
    search_finished = pyqtSignal()
    data_downloaded = pyqtSignal(object, QByteArray)
    error_occurred = pyqtSignal(object)

    def __init__(
            self, geometries, crop_type, sowing_date, map_product, sensor_type,
            start_date, end_date, mutex, n_planned_value=1.0, parent=None):
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
        self.start_date = start_date
        self.end_date = end_date
        self.mutex = mutex
        self.n_planned_value = n_planned_value
        self.parent = parent

        # setup coverage search filters
        date_filter = ''
        if self.start_date and self.end_date:
            date_filter = '$between:{}|{}'.format(
                self.start_date, self.end_date)
        elif self.end_date:
            date_filter = '$lte:{}'.format(self.end_date)

        # Disable filter when map product is Elevation
        self.filters = {}
        if self.map_product != ELEVATION['key']:
            if self.map_product == REFLECTANCE['key']:
                # Catalog-imagery API call. Maps.Type will be set to INSEASON_NDVI
                # This is a work-around provided by GeoSys, because reflectance results
                # are not shown in the respond from the API
                self.filters.update({
                    MAPS_TYPE: INSEASON_NDVI['key'],
                    IMAGE_DATE: date_filter
                })
                self.sensor_type and self.filters.update({
                    IMAGE_SENSOR: self.sensor_type
                })
            elif self.map_product == SOIL['key']:
                # This is a workaround to get the seasonfield ID
                # This has been suggested by GeoSys
                self.filters.update({
                    MAPS_TYPE: INSEASON_NDVI['key'],  # This is included for a shorter response
                    IMAGE_DATE: date_filter
                })
                self.sensor_type and self.filters.update({
                    IMAGE_SENSOR: self.sensor_type
                })
            else:
                # Coverage API call. Maps.Type should be included
                self.filters.update({
                    MAPS_TYPE: self.map_product,
                    IMAGE_DATE: date_filter
                })
                self.sensor_type and self.filters.update({
                    IMAGE_SENSOR: self.sensor_type
                })

        self.settings = QSettings()

        self.need_stop = False

    def run(self):
        """Start thread job."""
        self.search_started.emit()

        # search
        try:
            self.mutex.lock()

            searcher_client = BridgeAPI(
                *credentials_parameters_from_settings(),
                proxies=QGISSettings.get_qgis_proxy())

            collected_results = []
            for geometry in self.geometries:
                # Determines the approach required to do the coverage check
                if self.map_product == INSEASON_S2REP['key'] or self.map_product == REFLECTANCE['key'] or self.map_product == INSEASON_CVIN['key']:
                    # Makes use of the 'catalog-imagery' API calls
                    results = searcher_client.get_catalog_imagery(
                        geometry, self.crop_type, self.sowing_date,
                        filters=self.filters)
                elif self.map_product == INSEASONFIELD_AVERAGE_NDVI['key'] or self.map_product == INSEASONFIELD_AVERAGE_LAI['key'] or self.map_product == INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'] or self.map_product == INSEASONFIELD_AVERAGE_REVERSE_LAI['key']:
                    # Nitrogen maps should make use of the 'catalog-imagery' API calls
                    results = searcher_client.get_catalog_imagery(
                        geometry, self.crop_type, self.sowing_date,
                        filters=self.filters)
                else:
                    # Makes use of the 'coverage' API calls
                    results = searcher_client.get_coverage(
                        geometry, self.crop_type, self.sowing_date,
                        filters=self.filters)

                if isinstance(results, dict) and results.get('message'):
                    # TODO handle model_validation_error
                    raise Exception(results['message'])

                for result in results:
                    if self.need_stop:
                        break
                    # get thumbnail content
                    requested_map = None
                    for map_result in result['maps']:
                        if self.map_product == REFLECTANCE['key'] or self.map_product == SOIL['key']:
                            # Reflectance map and soil map type will make use of the INSEASON_NDVI to show coverage results
                            # This is a work-around provided by GeoSys
                            if map_result['type'] == INSEASON_NDVI['key']:
                                requested_map = map_result
                                break
                        else:  # Other map types
                            if map_result['type'] == self.map_product or (self.map_product == ELEVATION['key']):
                                requested_map = map_result
                                break

                    if not requested_map:
                        continue

                    if self.map_product == REFLECTANCE['key']:
                        # Reflectance map type should make use of the INSEASON_NDVI thumbnail
                        # This is a work-around provided by GeoSys
                        thumbnail_url = (
                                NDVI_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    date=result['image']['date']
                                ))
                    elif self.map_product == INSEASON_CVIN['key']:
                        thumbnail_url = (
                                CVIN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    image=result['image']['id']
                                ))
                    elif self.map_product == INSEASON_S2REP['key']:
                        thumbnail_url = (
                            S2REP_THUMBNAIL_URL.format(
                                bridge_url=searcher_client.bridge_server,
                                id=result['seasonField']['id'],
                                image=result['image']['id']
                            ))
                    elif self.map_product == INSEASONFIELD_AVERAGE_NDVI['key'] or self.map_product == INSEASONFIELD_AVERAGE_LAI['key'] or self.map_product == INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'] or self.map_product == INSEASONFIELD_AVERAGE_REVERSE_LAI['key']:
                        # Nitrogen map type
                        if self.map_product == INSEASONFIELD_AVERAGE_NDVI['key']:
                            # INSEASON AVERAGE NDVI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    image=result['image']['id'],
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_NDVI['key'],
                                    n_value=str(self.n_planned_value)
                                ))
                        elif self.map_product == INSEASONFIELD_AVERAGE_LAI['key']:
                            # INSEASON AVERAGE LAI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    image=result['image']['id'],
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_LAI['key'],
                                    n_value=str(self.n_planned_value)
                                ))
                        elif self.map_product == INSEASONFIELD_AVERAGE_REVERSE_NDVI['key']:
                            # INSEASON AVERAGE REVERSE NDVI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    image=result['image']['id'],
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
                                    n_value=str(self.n_planned_value)
                                ))
                        elif self.map_product == INSEASONFIELD_AVERAGE_REVERSE_LAI['key']:
                            # INSEASON AVERAGE REVERSE LAI
                            thumbnail_url = (
                                NITROGEN_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    image=result['image']['id'],
                                    nitrogen_map_type=INSEASONFIELD_AVERAGE_REVERSE_LAI['key'],
                                    n_value=str(self.n_planned_value)
                                ))
                    else:  # All other map types
                        thumbnail_url = (
                            requested_map['_links'].get('thumbnail') or (
                                NDVI_THUMBNAIL_URL.format(
                                    bridge_url=searcher_client.bridge_server,
                                    id=result['seasonField']['id'],
                                    date=result['image']['date']
                                )))

                    if thumbnail_url:
                        thumbnail_content = searcher_client.get_content(
                            thumbnail_url)
                        thumbnail_ba = QByteArray(thumbnail_content)
                    else:
                        thumbnail_ba = bytes('', 'utf-8')

                    collected_results.append({
                        'data': result,
                        'thumbnail': thumbnail_ba
                    })

            # Using this trick, rendering each list item will not be delayed
            # by thumbnail request.
            for result in collected_results:
                self.data_downloaded.emit(result['data'], result['thumbnail'])

            self.search_finished.emit()
        except:
            error_text = (self.tr(
                "Error of processing!\n{0}: {1}")).format(
                unicode(sys.exc_info()[0].__name__), unicode(
                    sys.exc_info()[1]))
            self.error_occurred.emit(error_text)
        finally:
            self.mutex.unlock()

    def stop(self):
        """Stop thread job."""
        self.need_stop = True


def create_map(
        map_specification,
        output_dir,
        filename,
        output_map_format,
        n_planned_value,
        data=None,
        params=None):
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
                "weather": "HOT",
                "soilMaterial": "BARE"
            }
            "type": "INSEASON_NDVI",
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
    :type n_planned_value: Numeric
    
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
    # Construct map creation parameters
    map_specification.update(map_specification['maps'][0])
    map_type_key = map_specification['type']
    season_field_id = map_specification['seasonField']['id']
    image_date = map_specification['image']['date']
    image_id = map_specification['image']['id']
    destination_base_path = os.path.join(output_dir, filename)
    data = data if data else {}
    params = params if params else {}
    data.update({'params': params})

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())
    field_map_json = bridge_api.get_field_map(
        map_type_key, season_field_id, image_date, image_id, n_planned_value, **data)

    return download_field_map(
        field_map_json=field_map_json,
        map_type_key=map_type_key,
        destination_base_path=destination_base_path,
        output_map_format=output_map_format,
        headers=bridge_api.headers,
        map_specification=map_specification,
        data=data,
        image_id=image_id)


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
                "weather": "HOT",
                "soilMaterial": "BARE"
            }
            "type": "INSEASON_NDVI",
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


def create_samz_map(
        season_field_id,
        list_of_image_date,
        output_dir,
        filename,
        output_map_format,
        data=None,
        params=None):
    """Create map based on given parameters.

    :param season_field_id: ID of the season field.
    :param season_field_id: str

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
    destination_base_path = os.path.join(output_dir, filename)
    data = data if data else {}
    params = params if params else {}
    data.update({'params': params})

    bridge_api = BridgeAPI(
        *credentials_parameters_from_settings(),
        proxies=QGISSettings.get_qgis_proxy())
    samz_map_json = bridge_api.get_samz_map(
        season_field_id, list_of_image_date, **data)

    return download_field_map(
        field_map_json=samz_map_json,
        map_type_key=map_type_key,
        destination_base_path=destination_base_path,
        output_map_format=output_map_format,
        headers=bridge_api.headers,
        data=data)


def download_field_map(
        field_map_json, map_type_key, destination_base_path,
        output_map_format, headers, map_specification=None, data=None, image_id=''):
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
                "weather": "HOT",
                "soilMaterial": "BARE"
            }
            "type": "INSEASON_NDVI",
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
    try:

        seasonfield_id = field_map_json['seasonField']['id']

        if map_type_key == REFLECTANCE['key']:
            # This is only for reflectance map type
            # Also, reflectance can ONLY make use of tiff.zip format

            # Retrieve the bridge server URL
            username, password, region, client_id, client_secret, use_testing_service = credentials_parameters_from_settings()
            bridge_server = (BRIDGE_URLS[region]['test']
                             if use_testing_service
                             else BRIDGE_URLS[region]['prod'])

            reflectance_map_family = REFLECTANCE['map_family']
            url = '{}/field-level-maps/v4/season-fields/{}/coverage/{}/{}/{}/image.tiff.zip'.format(bridge_server, seasonfield_id, image_id, reflectance_map_family['endpoint'], REFLECTANCE['key'])
        else:  # Other map types
            url = field_map_json['_links'][output_map_format['api_key']]

        char_question_mark = '?'  # Filtering char
        if char_question_mark in url:  # Filtering, which starts with '?' has already been added, so appending with '&'
            url = '{}&zoning=true&zoneCount={}'.format(
                url, data.get('zoneCount')) \
                if data.get('zoning') else url
        else:  # No filtering added yet, so appending with '?'
            url = '{}?zoning=true&zoneCount={}'.format(
                url, data.get('zoneCount')) \
                if data.get('zoning') else url
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
            fetch_data(url, zip_path, headers=headers)
            extract_zip(zip_path, destination_base_path)
        else:
            destination_filename = (
                    destination_base_path + output_map_format['extension'])
            fetch_data(url, destination_filename, headers=headers)
            if output_map_format == PNG or output_map_format == PNG_CC:
                # Download associated legend and world-file for geo-referencing
                # the PNG file.
                
                # This step check if the map type is color composition
                # If that is the case, legend will not be included to the items
                # list as the API does not include a legend for color composition
                if map_type_key == COLOR_COMPOSITION['key']:
                    list_items = [PGW]
                else:
                    list_items = [PGW, LEGEND]
                for item in list_items:
                    url = field_map_json['_links'][item['api_key']]

                    char_question_mark = '?'  # Filtering char
                    if char_question_mark in url:  # Filtering, which starts with '?' has already been added, so appending with '&'
                        url = '{}&zoning=true&zoneCount={}'.format(
                            url, data.get('zoneCount')) \
                            if data.get('zoning') else url
                    else:  # No filtering added yet, so appending with '?'
                        url = '{}?zoning=true&zoneCount={}'.format(
                            url, data.get('zoneCount')) \
                            if data.get('zoning') else url

                    destination_filename = '{}{}'.format(
                        destination_base_path, item['extension'])
                    fetch_data(url, destination_filename, headers=headers)
        # Get hotspots for zones if they have been requested by user.
        bridge_api = BridgeAPI(
            *credentials_parameters_from_settings(),
            proxies=QGISSettings.get_qgis_proxy())

        if data.get('zoning') and data.get('hotspot'):
            hotspot_per_part = False
            if data.get('zoningSegmentation'):
                hotspot_url = '{}?zoning=true&zoneCount={}&hotspot=true' \
                              '&zoningSegmentation=polygon'.format( \
                    field_map_json['_links']['self'], data.get('zoneCount'))

                hotspot_per_part = True
            else:
                hotspot_url = '{}?zoning=true&zoneCount={}&hotspot=true'. \
                    format(\
                    field_map_json['_links']['self'],
                    data.get('zoneCount'))

            hotspot_url = '{}&hotSpotPosition={}'.format(hotspot_url, data.get('position')) \
                if data.get('position') else hotspot_url
            hotspot_url = '{}&hotSpotFilter={}'.format(hotspot_url, data.get('filter')) \
                if data.get('filter') else hotspot_url

            map_json = bridge_api.get_hotspot(hotspot_url)

            output_dir = setting('output_directory', expected_type=str)

            if map_json.get('hotSpots'):
                if map_specification:
                    if hotspot_per_part:
                        hotspot_filename = 'HotspotsPerPart_{}_{}'.format(
                            map_specification['seasonField']['id'],
                            map_specification['image']['date']
                        )
                        hotspot_filename = check_if_file_exists(output_dir, hotspot_filename, SHP_EXT)
                    else:
                        hotspot_filename = 'HotspotsPerPolygon_{}_{}'.format(
                            map_specification['seasonField']['id'],
                            map_specification['image']['date']
                        )
                        hotspot_filename = check_if_file_exists(output_dir, hotspot_filename, SHP_EXT)
                create_hotspot_layer(
                    map_json.get('hotSpots'),
                    'hotspots',
                    hotspot_filename
                )

            if map_json.get('zones'):
                if map_specification:
                    if hotspot_per_part:
                        segment_filename = 'SegmentsPerPart_{}_{}'.format(
                            map_specification['seasonField']['id'],
                            map_specification['image']['date']
                        )
                        segment_filename = check_if_file_exists(output_dir, segment_filename, SHP_EXT)
                    else:
                        segment_filename = 'SegmentsPerPolygon_{}_{}'.format(
                            map_specification['seasonField']['id'],
                            map_specification['image']['date']
                        )
                        segment_filename = check_if_file_exists(output_dir, segment_filename, SHP_EXT)
                create_hotspot_layer(
                    map_json.get('zones'),
                    'segments',
                    segment_filename
                )
    except:
        # zip extraction error
        message = 'Failed to download file.'
        return False, message
    return True, message


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
