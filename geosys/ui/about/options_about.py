# coding=utf-8
"""About text for options dialog."""

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


def options_about():
    """About message for options dialog.

    .. versionadded:: 3.2.1

    :returns: A message object containing information for the about dialog.
    :rtype: messaging.message.Message
    """

    message = m.Message()
    message.add(m.Brand())
    message.add(heading())
    message.add(content())
    return message


def heading():
    """Method that returns just the header.

    This method was added so that the text could be reused in the
    other contexts.

    .. versionadded:: 3.2.2

    :returns: A heading object.
    :rtype: safe.messaging.heading.Heading
    """
    message = m.Heading(tr('GEOSYS Plugin about'), **SUBSECTION_STYLE)
    return message


def content():
    """Method that returns just the content.

    This method was added so that the text could be reused.

    .. versionadded:: 3.2.2

    :returns: A message object without brand element.
    :rtype: safe.messaging.message.Message
    """
    message = m.Message()
    message.add(m.Paragraph(tr(
        ' '
        '- EarthDaily agro https://earthdailyagro.com/\n '
        '- News https://earthdailyagro.com/news/\n '
        '- Careers https://earthdailyagro.com/careers/\n '
        '- Contact https://earthdailyagro.com/contact/\n '
        '- Twitter - https://twitter.com/EarthDailyAgro/\n '
        '- Linkedin - https://www.linkedin.com/company/115836/admin/\n '
        '- Youtube https://www.youtube.com/channel/UCy4X-hM2xRK3oyC_xYKSG_g'
    )))

    return message
