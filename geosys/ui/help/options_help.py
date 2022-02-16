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
    message = m.Heading(tr('GEOSYS Plugin options help'), **SUBSECTION_STYLE)
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
        'The GEOSYS Plugin options dialog is used to control various aspects '
        'of the Bridge API request settings. Here are brief descriptions of '
        'all the options available, grouped by the tab page on which they '
        'occur.'
    )))

    return message