# coding=utf-8
"""Help HTML utilities."""

from tempfile import mktemp

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices

# from geosys.ui.help.dock_help import dock_help
from geosys.utilities.resources import html_about_header, html_footer


def get_about_html(message=None):
    """Create the HTML content for the about dialog or for external browser

    :param message: An optional message object to display in the dialog.
    :type message: Message.Message

    :return: the about HTML content
    :rtype: str
    """

    html = html_about_header()

    # if message is None:
    #     message = dock_help()

    html += message.to_html()
    html += html_footer()

    return html


def show_about(message=None):
    """Open an about message in the user's browser

    :param message: An optional message object to display in the dialog.
    :type message: Message.Message
    """

    help_path = mktemp('.html')
    with open(help_path, 'wb+') as f:
        help_html = get_about_html(message)
        f.write(help_html.encode('utf8'))
        path_with_protocol = 'file://' + help_path
        QDesktopServices.openUrl(QUrl(path_with_protocol))
