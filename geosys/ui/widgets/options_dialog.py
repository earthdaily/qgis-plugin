# coding=utf-8
"""Implementation of GEOSYS options dialog.
"""
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QSettings

from geosys.bridge_api_wrapper import BridgeAPI
from geosys.utilities.resources import get_ui_class
from geosys.utilities.settings import set_setting, setting

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
            'geosys_region_eu': self.eu_radio_button,
            'save_credentials': self.save_credentials_checkbox,
            'use_testing_service': self.testing_service_checkbox
        }
        self.credentials_settings = {
            'bridge_api_username': self.username_form,
            'bridge_api_password': self.password_form
        }
        self.text_settings = {
            'bridge_api_page_limit': self.page_limit_form
        }
        self.text_settings.update(self.credentials_settings)
        self.combo_box_settings = {
            'crop_type': self.crop_combo_box
        }
        self.date_settings = {
            'sowing_date': self.sowing_date_edit
        }

        # Populate crop combo box
        self.crops = BridgeAPI.get_crops()
        for crop in self.crops:
            self.crop_combo_box.addItem(crop)

        # Restore state from setting
        self.restore_settings()

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
        message_title = "Bridge API Authentication Status"
        try:
            bridge_api = BridgeAPI(
                username=self.username(),
                password=self.password(),
                region=self.region(),
                use_testing_service=self.use_testing_service())

            if not bridge_api.authenticated:
                QMessageBox.critical(
                    self, message_title, bridge_api.authentication_message)
            else:
                QMessageBox.information(
                    self, message_title, bridge_api.authentication_message)
        except Exception as e:
            QMessageBox.critical(self, message_title, str(e))

    def restore_boolean_setting(self, key, check_box):
        """Set check_box according to setting of key.

        :param key: Key to retrieve setting value.
        :type key: str

        :param check_box: Check box to show and set the setting.
        :type check_box: PyQt5.QtWidgets.QCheckBox.QCheckBox
        """
        flag = setting(key, expected_type=bool, qsettings=self.settings)
        check_box.setChecked(flag)

    def restore_text_setting(self, key, line_edit):
        """Set line_edit text according to setting of key.

        :param key: Key to retrieve setting value.
        :type key: str

        :param line_edit: Line edit for user to edit the setting
        :type line_edit: PyQt5.QtWidgets.QLineEdit.QLineEdit
        """
        value = setting(key, expected_type=str, qsettings=self.settings)
        line_edit.setText(value)

    def restore_combo_box_setting(self, key, combo_box):
        """Set combo_box index according to setting of key.

        :param key: Key to retrieve setting value.
        :type key: str

        :param combo_box: Combo box for user to edit the setting
        :type combo_box: PyQt5.QtWidgets.QComboBox.QComboBox
        """
        value = setting(key, expected_type=str, qsettings=self.settings)
        if value:
            for index in range(0, combo_box.count()):
                item = combo_box.itemText(index)
                if item == value:
                    combo_box.setCurrentIndex(index)
                    break

    def restore_date_setting(self, key, date_edit):
        """Set date_edit index according to setting of key.

        :param key: Key to retrieve setting value.
        :type key: str

        :param date_edit: Combo box for user to edit the setting
        :type date_edit: PyQt5.QtWidgets.QDateEdit.QDateEdit
        """
        value = setting(key, expected_type=str, qsettings=self.settings)
        if value:
            date = QDate.fromString(value, 'yyyy-MM-dd')
            date_edit.setDate(date)

    def restore_settings(self):
        """Reinstate the options based on the user's stored session info."""
        # Restore boolean setting as check box.
        for key, check_box in list(self.boolean_settings.items()):
            self.restore_boolean_setting(key, check_box)

        # Restore text setting as line edit.
        for key, line_edit in list(self.text_settings.items()):
            self.restore_text_setting(key, line_edit)

        # Restore text setting as combo box.
        for key, combo_box in list(self.combo_box_settings.items()):
            self.restore_combo_box_setting(key, combo_box)

        # Restore date setting as date edit.
        for key, date_edit in list(self.date_settings.items()):
            self.restore_date_setting(key, date_edit)

    def save_boolean_setting(self, key, check_box):
        """Save boolean setting according to check_box state.

        :param key: Key to retrieve setting value.
        :type key: str

        :param check_box: Check box to show and set the setting.
        :type check_box: PyQt5.QtWidgets.QCheckBox.QCheckBox
        """
        set_setting(key, check_box.isChecked(), qsettings=self.settings)

    def save_text_setting(self, key, line_edit):
        """Save text setting according to line_edit value.

        :param key: Key to retrieve setting value.
        :type key: str

        :param line_edit: Line edit for user to edit the setting
        :type line_edit: PyQt5.QtWidgets.QLineEdit.QLineEdit
        """
        set_setting(key, line_edit.text(), self.settings)

    def save_combo_box_setting(self, key, combo_box):
        """Save combo_box setting according to line_edit value.

        :param key: Key to retrieve setting value.
        :type key: str

        :param combo_box: Line edit for user to edit the setting
        :type combo_box: PyQt5.QtWidgets.QComboBox.QComboBox
        """
        set_setting(key, combo_box.currentText(), self.settings)

    def save_date_setting(self, key, date_edit):
        """Save combo_box setting according to line_edit value.

        :param key: Key to retrieve setting value.
        :type key: str

        :param date_edit: Line edit for user to edit the setting
        :type date_edit: PyQt5.QtWidgets.QDateEdit.QDateEdit
        """
        date = date_edit.date()
        set_setting(key, date.toString('yyyy-MM-dd'), self.settings)

    def save_settings(self):
        """Store the options into the user's stored session info."""
        # Redefine to avoid mutable object
        text_settings = dict(self.text_settings)

        # Save boolean settings
        for key, check_box in list(self.boolean_settings.items()):
            self.save_boolean_setting(key, check_box)

        if not self.save_credentials_checkbox.isChecked():
            for key in self.credentials_settings.keys():
                del text_settings[key]
                set_setting(key, '')

        # Save text settings
        for key, line_edit in list(self.text_settings.items()):
            self.save_text_setting(key, line_edit)

        # Save combo box settings
        for key, combo_box in list(self.combo_box_settings.items()):
            self.save_combo_box_setting(key, combo_box)

        # Save date settings
        for key, date_edit in list(self.date_settings.items()):
            self.save_date_setting(key, date_edit)

    def accept(self):
        """Method invoked when OK button is clicked."""
        self.save_settings()
        super(GeosysOptionsDialog, self).accept()
