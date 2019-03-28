# coding=utf-8
"""Implementation of custom GEOSYS item widget.
"""
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QSizePolicy, QGridLayout)

from qgis.PyQt.QtCore import Qt

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class CoverageSearchResultItemWidget(QWidget):
    """Custom item widget for coverage search results."""

    def __init__(self, coverage_map_json, thumbnail_ba, parent=None):
        """Custom item widget for coverage search results.

        :param coverage_map_json: Result of single map coverage.
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
                },
                "maps": [
                    {
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
                        }
                    }
                ],
                "coverageType": "CLEAR"
            }
        :type coverage_map_json: dict

        :param thumbnail_ba: Thumbnail image data in byte array format.
        :type thumbnail_ba: QByteArray

        :param parent: Parent class.
        :type parent: QWidget
        """
        super(CoverageSearchResultItemWidget, self).__init__(parent)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 10, 5, 10)
        self.setLayout(self.layout)

        self.map_thumbnail = QLabel(self)
        self.map_thumbnail.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.map_thumbnail.resize(24, 24)

        qimg = QImage.fromData(thumbnail_ba)
        pixmap = QPixmap.fromImage(qimg)
        self.map_thumbnail.setPixmap(pixmap)
        self.layout.addWidget(self.map_thumbnail)

        self.map_description_layout = QGridLayout(self)
        self.map_description_layout.setSpacing(0)
        self.layout.addLayout(self.map_description_layout)

        season_field_id = coverage_map_json.get(
            'seasonField', {}).get('id', '')
        self.season_field_id = QLabel(self)
        self.season_field_id.setTextFormat(Qt.RichText)
        self.season_field_id.setWordWrap(True)
        self.season_field_id.setText(
            u"   <strong> {} </strong>".format(season_field_id))
        self.map_description_layout.addWidget(self.season_field_id, 0, 0, 1, 3)

        image_description = coverage_map_json.get('image', {})
        self.image_date = QLabel(self)
        self.image_date.setTextFormat(Qt.RichText)
        self.image_date.setWordWrap(True)
        self.image_date.setText(image_description.get('date', ''))
        self.map_description_layout.addWidget(self.image_date, 1, 0)

        self.image_sensor = QLabel(self)
        self.image_sensor.setTextFormat(Qt.RichText)
        self.image_sensor.setWordWrap(True)
        self.image_sensor.setText(image_description.get('sensor', ''))
        self.map_description_layout.addWidget(self.image_sensor, 2, 0)

        self.coverage_type = QLabel(self)
        self.coverage_type.setTextFormat(Qt.RichText)
        self.coverage_type.setWordWrap(True)
        self.coverage_type.setText(coverage_map_json.get('coverageType', ''))
        self.map_description_layout.addWidget(self.coverage_type, 3, 0)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.coverage_map_json = coverage_map_json
        self.thumbnail_ba = thumbnail_ba

    def mouseDoubleClickEvent(self, event):
        self.addToMap()
