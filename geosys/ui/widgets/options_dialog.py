# coding=utf-8
"""Implementation of GEOSYS options dialog.
"""
from PyQt5 import QtGui, QtWidgets
from qgis.PyQt.QtCore import QSettings

from geosys.bridge_api_wrapper import BridgeAPI
from geosys.utilities.resources import get_ui_class

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

FORM_CLASS = get_ui_class('options_dialog_base.ui')


class GeosysOptionsDialog(QtWidgets.QDialog, FORM_CLASS):
    """Options dialog for the GEOSYS plugin."""

    def __init__(self, iface, parent=None):
        """Constructor"""
        super(GeosysOptionsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Save reference to the QGIS interface and parent
        self.iface = iface
        self.parent = parent
        self.settings = QSettings()

        # List of setting key and control
        self.boolean_settings = {
            'geosys_region_na': self.us_radio_button,
            'geosys_region_eu': self.eu_radio_button
        }

        self.text_settings = {
            'bridge_api_username': self.username_form,
            'bridge_api_password': self.password_form,
            'bridge_api_page_limit': self.page_limit_form
        }

        self.us_radio_button.setChecked(True)
        self.connect_button.clicked.connect(self.request_token)

    def username(self):
        """Get current value of username."""
        return self.username_form.text()

    def password(self):
        """Get current value of password."""
        return self.password_form.text()

    def region(self):
        """Get current value of region."""
        if self.eu_radio_button.isChecked():
            return 'eu'
        return 'na'

    def use_testing_service(self):
        """Testing service flag."""
        return self.testing_service_checkbox.isChecked()

    def request_token(self):
        """Request access token to GEOSYS's identity server."""
        bridge_api = BridgeAPI(
            username=self.username(),
            password=self.password(),
            region=self.region(),
            use_testing_service=self.use_testing_service())

        QtWidgets.QMessageBox.information(
            self, "Bridge API Authentication Status",
            bridge_api.authentication_message)
