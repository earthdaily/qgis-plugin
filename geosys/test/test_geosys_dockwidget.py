# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

import unittest

from geosys.test.utilities import get_qgis_app
from geosys.ui.widgets.geosys_dockwidget import GeosysPluginDockWidget
from PyQt5.QtWidgets import QComboBox

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

QGIS_APP = get_qgis_app()


class GeosysPluginDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = GeosysPluginDockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

    def test_clear_combo_box(self):
        """Test if the clear_combo_box method works as it should."""

        test_list = ['First', 'Second', 'Third']
        test_cb = QComboBox()
        test_cb.addItems(test_list)

        GeosysPluginDockWidget.clear_combo_box(test_cb)

        expected_count = 0
        cb_count = test_cb.count()

        message = 'Expected %s items in the combobox, but got %s' % (expected_count, str(cb_count))
        self.assertEqual(expected_count, str(cb_count), message)


if __name__ == "__main__":
    suite = unittest.makeSuite(GeosysPluginDockWidgetTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
