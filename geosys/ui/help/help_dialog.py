# coding=utf-8
"""Help Dialog."""

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # NOQA pylint: disable=unused-import
from qgis.PyQt import QtGui, QtWidgets, QtWebKitWidgets
from qgis.PyQt.QtCore import Qt

from geosys.utilities.help import get_help_html
from geosys.utilities.resources import get_ui_class, resources_path

FORM_CLASS = get_ui_class('help_dialog_base.ui')

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = '$Format:%H$'


class HelpDialog(QtWidgets.QDialog, FORM_CLASS):
    """About dialog for the GEOSYS plugin."""

    def __init__(self, parent=None, message=None):
        """Constructor for the dialog.

        :param message: An optional message object to display in the dialog.
        :type message: Message.Message

        :param parent: Parent widget of this dialog
        :type parent: QWidget
        """

        QtWidgets.QDialog.__init__(
            self, parent,
            flags=Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        self.parent = parent
        icon = resources_path('img', 'icons', 'icon.png')
        self.setWindowIcon(QtGui.QIcon(icon))

        # Make the html links open on the default browser instead
        # of opening the current help dialog.
        self.help_web_view.page().setLinkDelegationPolicy(
            QtWebKitWidgets.QWebPage.DelegateAllLinks
        )
        self.help_web_view.linkClicked.connect(self.link_clicked)

        self.help_web_view.setHtml(get_help_html(message))

    def link_clicked(self, url):
        QtGui.QDesktopServices.openUrl(url)
