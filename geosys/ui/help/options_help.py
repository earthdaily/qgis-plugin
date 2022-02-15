# coding=utf-8
"""Help text for options dialog."""

from geosys import messaging as m
from geosys.messaging import styles
from geosys.utilities.i18n import tr
from geosys.utilities.resources import resources_path

SUBSECTION_STYLE = styles.SUBSECTION_LEVEL_3_STYLE
INFO_STYLE = styles.BLUE_LEVEL_4_STYLE
SMALL_ICON_STYLE = styles.SMALL_ICON_STYLE

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = '$Format:%H$'


def options_help():
    """Help message for options dialog.

    .. versionadded:: 3.2.1

    :returns: A message object containing helpful information.
    :rtype: messaging.message.Message
    """

    message = m.Message()
    message.add(m.Brand())
    message.add(heading())
    message.add(content())
    return message


def heading():
    """Helper method that returns just the header.

    This method was added so that the text could be reused in the
    other contexts.

    .. versionadded:: 3.2.2

    :returns: A heading object.
    :rtype: safe.messaging.heading.Heading
    """
    message = m.Heading(tr('GEOSYS QGIS plugin dock help'), **SUBSECTION_STYLE)
    return message


def content():
    """Helper method that returns just the content.

    This method was added so that the text could be reused in the
    dock_help module.

    .. versionadded:: 3.2.2

    :returns: A message object without brand element.
    :rtype: safe.messaging.message.Message
    """
    message = m.Message()
    message.add(m.Paragraph(tr(
        '<b>Select a coverage boundary from active layers</b> '
        '<p>Choose a polygon layer with one or more polygons representing the area or '
        'areas you are interested in for retrieving the sensor data. If you have a selection '
        'on that layer, only the selected polygons will be used. If you have more than 10 '
        'polygons, only the first 10 polygons will be processed.</p> '
        ' '
        '<b>Choose a map product type</b>'
        '<ul> '
        '<li><b>COLORCOMPOSITION</b> - </li>'
        '<li><b>ELEVATION</b> - Height above sea level in meters.</li>'
        '<li><b>INSEASON_CVI</b> - </li>'
        '<li><b>INSEASON_CVIN</b> - Provides the in-season Chlorophyll Vegetation Index normalized.</li>'
        '<li><b>INSEASON_EVI</b> - Provides the in-season enhanced vegetation index (EVI).</li>'
        '<li><b>INSEASON_GNDVI</b> - Provides the in-season green normalized difference vegetation index (GNDVI).</li>'
        '<li><b>INSEASON_LAI</b> - Provides the in-season leaf area index (LAI). It is used as an indicator of the amount of leaf material.</li>'
        '<li><b>INSEASON_NDVI</b> - Provides the in-season normalized difference vegetation index (NDVI).</li>'
        '<li><b>INSEASON_S2REP</b> - Provides the in-season S2REP Index. Generates a map according to the amount of chlorophyll content per unit of leaf (LCC).</li>'
        '<li><b>INSEASONFIELD_AVERAGE_NDVI</b> - Provides the input map and the variable-rate application map based on NDVI map to better inform input placement.</li>'
        '<li><b>INSEASONFIELD_AVERAGE_LAI</b> - Provides the input map and the variable-rate application map based on LAI map to better inform input placement.</li>'
        '<li><b>INSEASONFIELD_AVERAGE_REVERSE_NDVI</b> - Provides the input map and the variable-rate application map based on NDVI map to better inform input placement.</li>'
        '<li><b>INSEASONFIELD_AVERAGE_REVERSE_LAI</b> - Provides the input map and the variable-rate application map based on LAI map to better inform input placement.</li>'
        '<li><b>INSEASONPARTIAL_EVI</b> - Provides the in-season partial enhanced vegetation index (EVI).</li>'
        '<li><b>INSEASONPARTIAL_NDVI</b> - Provides the in-season partial normalized difference vegetation index (NDVI).</li>'
        '<li><b>OM</b> - </li>'
        '<li><b>REFLECTANCE</b> - Provides the Reflectance map at Top of Canopy for Sentinel 2 and Lansat-8.</li>'
        '<li><b>Soil</b> - Provides the in-season Soil type map. Can be generate only in the USA, contains information about soil as collected by the National Cooperative Soil Survey.</li>'
        '<li><b>SAMZ</b> - </li>'
        '<li><b>YGM</b> - </li>'
        '<li><b>YPM</b> - </li>'
        '</ul> '
        ' '
        '<b>Choose a sensor</b>'
        '<ul> '
        '<li><b>DEIMOS-1</b> - Commercial data at 22 m ground resolution with an approximate 2-day revisit (combined).</li>'
        '<li><b>ALSAT-1B</b> - Algeria Satellite-1B with a spatial resolution at 24 m ground resolution, up to 3 days of revisit.</li>'
        '<li><b>GAOFEN-1 and GAOFEN-6</b> - Both has a ground resolution equal to 16 meters with a revisited equal to 4 days.</li>'
        '<li><b>CBERS-4 (MUXCam)</b> - The China-Brazil Earth Resources Satellite Program with 20 meters spatial resolution and a revisit capacity of 26 days. Images are available only in Brazil via the Geosys virtual constellation.</li>'
        '<li><b>LANDSAT-8 and LANDSAT-9</b> - Providing moderate-resolution imagery at 30 meters resampled to 15 meters by Geosys. Revisiting every 16 days.</li>'
        '<li><b>RESOURCESAT2</b> - The Linear Imaging Self-Scanning Sensor (LISS-III) with 23.5-meter spatial resolution LISS-IV Camera with 5.8-meter spatial resolution. Revisiting every 24 days.</li>'
        '<li><b>SENTINEL-2</b> - Spatial resolution of 10 m. Revisiting every 5 days under the same viewing angles. Multi-spectral data with 13 bands in the visible, near infrared, and short-wave infrared part of the spectrum.</li>'
        '</ul> '
    )))

    return message
