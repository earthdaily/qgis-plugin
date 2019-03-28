# coding=utf-8
"""Implementation of custom GEOSYS item widget.
"""
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QByteArray, QSettings

from geosys.bridge_api.default import MAPS_TYPE, IMAGE_SENSOR, IMAGE_DATE
from geosys.bridge_api_wrapper import BridgeAPI
from geosys.utilities.settings import setting

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


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
        self.filters = {
            MAPS_TYPE: self.map_product,
            IMAGE_SENSOR: self.sensor_type,
            IMAGE_DATE: '$between:{}|{}'.format(self.start_date, self.end_date)
        }

        self.settings = QSettings()

        # define credentials
        username = setting(
            'bridge_api_username',
            expected_type=str, qsettings=self.settings)
        password = setting(
            'bridge_api_password',
            expected_type=str, qsettings=self.settings)
        client_id = setting(
            'bridge_api_client_id',
            expected_type=str, qsettings=self.settings)
        client_secret = setting(
            'bridge_api_client_secret',
            expected_type=str, qsettings=self.settings)

        # define geosys region
        is_region_eu = setting(
            'geosys_region_eu',
            expected_type=bool, qsettings=self.settings)
        region = 'eu' if is_region_eu else 'na'

        # define prod or testing service
        use_testing_service = setting(
            'use_testing_service',
            expected_type=bool, qsettings=self.settings)

        self.searcher_client = BridgeAPI(
            username, password, region, client_id, client_secret,
            use_testing_service=use_testing_service)
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

                thumbnail_url = requested_map['_links']['thumbnail']
                thumbnail_content = self.searcher_client.get_content(
                    thumbnail_url)
                thumbnail_ba = QByteArray(thumbnail_content)

                collected_results.append({
                    'data': result,
                    'thumbnail': thumbnail_ba
                })

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
            self.error_occurred.emit(error_text)
            raise e

        self.mutex.unlock()

    def stop(self):
        """Stop thread job."""
        self.need_stop = True
