# coding=utf-8
"""Implementation of custom GEOSYS coverage downloader.
"""
import os
import sys
import tempfile

from PyQt5.QtCore import QThread, pyqtSignal, QByteArray, QSettings

from geosys.bridge_api.default import MAPS_TYPE, IMAGE_SENSOR, IMAGE_DATE, \
    ZIPPED_SHP, ZIPPED_TIFF, SHP_EXT, TIFF_EXT
from geosys.bridge_api_wrapper import BridgeAPI
from geosys.utilities.downloader import fetch_zip, extract_zip
from geosys.utilities.settings import setting

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
            self, geometry, crop_type, sowing_date, map_product, sensor_type,
            start_date, end_date, mutex, parent=None):
        """Thread object wrapper for coverage search.

        :param geometry: Geometry filter in WKT format.
        :type geometry: str

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

        :param parent: Parent class.
        :type parent: QWidget
        """
        super(CoverageSearchThread, self).__init__(parent)
        self.geometry = geometry
        self.crop_type = crop_type
        self.sowing_date = sowing_date
        self.map_product = map_product
        self.sensor_type = sensor_type
        self.start_date = start_date
        self.end_date = end_date
        self.mutex = mutex
        self.parent = parent

        # setup coverage search filters
        date_filter = ''
        if self.start_date and self.end_date:
            date_filter = '$between:{}|{}'.format(
                self.start_date, self.end_date)
        elif self.end_date:
            date_filter = '$lte:{}'.format(self.end_date)

        self.filters = {
            MAPS_TYPE: self.map_product,
            IMAGE_SENSOR: self.sensor_type,
            IMAGE_DATE: date_filter
        }

        self.settings = QSettings()

        self.searcher_client = BridgeAPI(
            *credentials_parameters_from_settings())
        # TODO set QGIS proxy to the searcher

        self.need_stop = False

    def run(self):
        """Start thread job."""
        self.search_started.emit()

        # search
        try:
            self.mutex.lock()
            results = self.searcher_client.get_coverage(
                self.geometry, self.crop_type, self.sowing_date,
                filters=self.filters)

            if isinstance(results, dict) and results.get('message'):
                # TODO handle model_validation_error
                raise Exception(results['message'])

            collected_results = []
            for result in results:
                if self.need_stop:
                    break
                # get thumbnail content
                requested_map = None
                for map_result in result['maps']:
                    if map_result['type'] == self.map_product:
                        requested_map = map_result
                        break

                if not requested_map:
                    continue

                thumbnail_url = requested_map['_links'].get('thumbnail')
                if thumbnail_url:
                    thumbnail_content = self.searcher_client.get_content(
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
        except Exception:
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
        map_specifications,
        output_dir,
        filename,
        vector_format=False,
        data=None,
        params=None):
    """Create map based on given parameters.

    :param map_specifications: Result of single map coverage specifications.
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
    :type map_specifications: dict

    :param output_dir: Base directory of the output.
    :type output_dir: str
    
    :param filename: Filename of the output.
    :type filename: str
    
    :param vector_format: Flag indicating to create the map in vector format.
        If this set to False (default value), it will create map in 
        raster format.
    :type vector_format: bool
    
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
    map_type_key = map_specifications['type']
    season_field_id = map_specifications['seasonField']['id']
    image_date = map_specifications['image']['date']
    data = data if data else {}
    params = params if params else {}
    data.update(params)

    bridge_api = BridgeAPI(*credentials_parameters_from_settings())
    field_map_json = bridge_api.get_field_map(
        map_type_key, season_field_id, image_date, **data)

    message = 'Field map successfully created.'
    if not field_map_json.get('seasonField'):
        # field map request error
        message = 'Field map request failed.'
        if field_map_json.get('message'):
            message = '{} {}'.format(message, field_map_json['message'])
        return False, message

    # If request succeeded, download zipped map and extract it
    # in requested format.
    map_format = ZIPPED_SHP if vector_format else ZIPPED_TIFF
    map_extension = SHP_EXT if vector_format else TIFF_EXT
    zip_path = tempfile.mktemp('{}.zip'.format(map_extension))
    url = field_map_json['_links'][map_format]
    try:
        fetch_zip(url, zip_path, headers=bridge_api.headers)
        extract_zip(zip_path, os.path.join(output_dir, filename))
    except:
        # zip extraction error
        message = 'Failed to extract zip file.'
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
