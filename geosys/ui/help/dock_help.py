# coding=utf-8
"""Help text for the dock widget."""

from geosys import messaging as m
from geosys.bridge_api.default import MAX_FEATURE_NUMBERS
from geosys.bridge_api.definitions import SENSORS, ARCHIVE_MAP_PRODUCTS
from geosys.messaging import styles
from geosys.utilities.i18n import tr

SUBSECTION_STYLE = styles.SUBSECTION_LEVEL_3_STYLE
INFO_STYLE = styles.BLUE_LEVEL_4_STYLE
SMALL_ICON_STYLE = styles.SMALL_ICON_STYLE

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = '$Format:%H$'


def dock_help():
    """Help message for Dock Widget.

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

    paragraph = m.Paragraph(tr(
        m.ImportantText(tr(
            'Select a coverage boundary from active layers'
        )).to_html()
    ))
    message.add(paragraph)

    paragraph = m.Paragraph(tr(
        'Choose a polygon layer with one or more polygons representing '
        'the area or areas you are interested in for retrieving '
        'the sensor data. If you have a selection on that layer, '
        'only the selected polygons will be used. If you have more than '
        '{max_features} polygons, only the first {max_features} polygons '
        'will be processed.'
    ).format(max_features=MAX_FEATURE_NUMBERS))
    message.add(paragraph)

    paragraph = m.Paragraph(
        m.ImportantText(tr(
            'Choose a map product type'
        )).to_html()
    )
    message.add(paragraph)

    bullets = m.BulletedList()
    for map_product in ARCHIVE_MAP_PRODUCTS:
        bullets.add(m.Text(
            '{} - {}'.format(
                m.ImportantText(tr(
                    map_product['name']
                )).to_html(),
                map_product['description'])
        ))
    message.add(bullets)

    paragraph = m.Paragraph(tr(
        m.ImportantText(tr(
            'Choose a sensor type'
        )).to_html()
    ))
    message.add(paragraph)

    bullets = m.BulletedList()
    for sensor in SENSORS:
        bullets.add(m.Text(
            '{} - {}'.format(
                m.ImportantText(tr(
                    sensor['name']
                )).to_html(),
                sensor['description'])
        ))
    message.add(bullets)

    paragraph = m.Paragraph(tr(
        m.ImportantText(tr(
            'Choose a start and end date'
        )).to_html()
    ))
    message.add(paragraph)

    paragraph = m.Paragraph(tr(
        'The date range of the images to be retrieved.'
    ))
    message.add(paragraph)

    spotlight_paragraph = m.Paragraph(tr(
        '<p> The <b> Geosys API </b> developer portal is available here'
        '<a href="https://developer.geosys.com" > https://developer.geosys.com</a></p>'
    ))

    message.add(spotlight_paragraph)

    return message
