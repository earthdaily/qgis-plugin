# coding=utf-8
"""About text for options dialog."""

import os
from geosys import messaging as m
from geosys.messaging.item import image
from geosys.messaging import styles
from geosys.utilities.i18n import tr
from geosys.utilities.resources import resources_path, resource_url

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

    # Social media icons for use in the about dialog
    icon_instagram = resources_path('img', 'icons_about', 'jpg', 'instagram.jpg')
    icon_linkedin = resources_path('img', 'icons_about', 'jpg', 'linkedin.jpg')
    icon_twitter = resources_path('img', 'icons_about', 'jpg', 'twitter.jpg')
    icon_youtube = resources_path('img', 'icons_about', 'jpg', 'youtube.jpg')
    icon_whatsapp = resources_path('img', 'icons_about', 'jpg', 'whatsapp.jpg')

    # Adds the icons to the about dialog
    message.add(m.Image(resource_url(icon_instagram), "instagram.jpg", 35, 35, ""))
    message.add(m.Image(resource_url(icon_linkedin), "linkedin.jpg", 35, 35, "https://www.linkedin.com/company/115836/admin/"))
    message.add(m.Image(resource_url(icon_twitter), "twitter.jpg", 35, 35, "https://twitter.com/EarthDailyAgro/"))
    message.add(m.Image(resource_url(icon_youtube), "youtube.jpg", 35, 35, "https://www.youtube.com/channel/UCy4X-hM2xRK3oyC_xYKSG_g"))
    message.add(m.Image(resource_url(icon_whatsapp), "whatsapp.jpg", 35, 35, ""))

    return message


def heading():
    """Method that returns just the header.

    This method was added so that the text could be reused in the
    other contexts.

    .. versionadded:: 3.2.2

    :returns: A heading object.
    :rtype: safe.messaging.heading.Heading
    """
    message = m.Heading(tr('About EarthDaily Agro'), **SUBSECTION_STYLE)
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
        '<ul> '
        '<p><b>EarthDaily Agro is the agricultural analysis division '
        'of EarthDaily Analytics. '
        'Learn more about EarthDaily at <a href="https://earthdailyagro.com/"> earthdaily.com</a></b></p>'
        ' '
        '<p>EarthDaily Agro uses satellite imaging to provide '
        'advanced analytics to mitigrate risk and the planet. '
        'Increase efficienies - leading to more sustainable '
        'outcomes for the organization and people who '
        'feed.</p> '
        '</ul>'
    )))

    return message
