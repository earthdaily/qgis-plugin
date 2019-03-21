# coding=utf-8
"""Implementation of GEOSYS options dialog.
"""
from PyQt5 import QtGui, QtWidgets

from geosys.utilities.resources import get_ui_class

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

FORM_CLASS = get_ui_class('options_dialog_base.ui')


class GeosysOptionsDialog(QtWidgets.QDialog, FORM_CLASS):
    """Options dialog for the GEOSYS plugin."""

    def __init__(self, parent=None):
        """Constructor"""
        super(GeosysOptionsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
