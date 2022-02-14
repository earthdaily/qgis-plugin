# coding=utf-8
"""About text for options dialog."""

import os
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
    message = m.Heading(tr('About EarthDaily Agro'), **SUBSECTION_STYLE)
    return message


def social_media_icon(*args):
    """Get the path to our resources folder.

    Note that in version 3.0 we removed the use of Qt Resource files in
    favour of directly accessing on-disk resources.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = os.path.dirname(__file__)
    path = os.path.abspath(
        os.path.join(path, os.path.pardir, 'resources'))
    for item in args:
        path = os.path.abspath(os.path.join(path, item))

    return path


def to_html(uri, text, html_attributes):
    """Render as html.
    """
    return '<img src="%s" title="%s" alt="%s" %s/>' % (
        uri,
        text,
        text,
        html_attributes)

def content():
    """Method that returns just the content.

    This method was added so that the text could be reused.

    .. versionadded:: 3.2.2

    :returns: A message object without brand element.
    :rtype: safe.messaging.message.Message
    """
    # Social media icons for use in the about dialog
    icon_instagram = resources_path('img', 'icons_about', 'instagram.svg')
    icon_linkedin = resources_path('img', 'icons_about', 'jpg', 'linkedin.jpg')
    icon_twitter = resources_path('img', 'icons_about', 'twitter.svg')
    icon_youtube = resources_path('img', 'icons_about', 'youtube.svg')

    print("dir: " + str(icon_linkedin))

    message = m.Message()

    message.add(

        #'<ul>'
        '<img src="C:/Users/Divan/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/qgis-plugin/geosys/resources/img/icons_about/jpg/linkedin.jpg" />'
        #'</ul>'

        # '<ul> '
        # '<p><b>EarthDaily Agro is the agricultural analysis division '
        # 'of EarthDaily Analytics. '
        # 'Learn more about EarthDaily at <a href="https://earthdailyagro.com/"> earthdaily.com</a></b></p>'
        # ' '
        # '<p>EarthDaily Agro uses satellite imaging to provide '
        # 'advanced analytics to mitigrate risk and the planet. '
        # 'Increase efficienies - leading to more sustainable '
        # 'outcomes for the organization and people who '
        # 'feed.</p> '
        # ' '
        # '<a href="https://www.linkedin.com/company/115836/admin/">'
        # '<img alt="png" height="36" src=' + icon_linkedin + ' width="36">'
        # '</a>'
        # ' '
        # '<li>EarthDaily agro: <a href="https://earthdailyagro.com/"> https://earthdailyagro.com/</a></li> '
        # '<li>Contact: <a href="https://earthdailyagro.com/contact/"> https://earthdailyagro.com/contact/</a></li> '
        # '<li>Twitter: <a href="https://twitter.com/EarthDailyAgro/"> https://twitter.com/EarthDailyAgro/</a></li> '
        # '<li>Linkedin: <a href="https://www.linkedin.com/company/115836/admin/"> https://www.linkedin.com/company/115836/admin/</a></li> '
        # '<li>YouTube: <a href="https://www.youtube.com/channel/UCy4X-hM2xRK3oyC_xYKSG_g"> https://www.youtube.com/channel/UCy4X-hM2xRK3oyC_xYKSG_g</a></li> '
        # '</ul>'
    )

    return message
