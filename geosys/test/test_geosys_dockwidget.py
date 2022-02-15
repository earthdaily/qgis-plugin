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
from geosys.utilities.settings import setting
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

        test_list = ['First', 'Second', 'Third']  # A list of items which will be added to the combobox
        test_cb = QComboBox()
        test_cb.addItems(test_list)

        # Clears the combobox of all items
        GeosysPluginDockWidget.clear_combo_box(self.dockwidget, test_cb)

        expected_count = 0  # The combobox should now be empty
        cb_count = test_cb.count()

        message = 'Expected %s items in the combobox, but got %s' % (str(expected_count), str(cb_count))
        self.assertEqual(str(expected_count), str(cb_count), message)

    def test_populate_map_products(self):
        """Test whether the combobox is populated correctly.
        If the zone is set to US, the soil map type can be included.
        If the zone is set to EU, the soil map type should be excluded.
        """

        GeosysPluginDockWidget.populate_map_products(self.dockwidget)

        key_us = 'geosys_region_na'
        us_option = setting(key_us, expected_type=bool, qsettings=self.dockwidget.settings)
        if us_option:  # Expected number of items for US (soil map included)
            expected_count = 21
        else:  # Expected number of items for EU (soil map excluded)
            expected_count = 20

        combobox = self.dockwidget.map_product_combo_box
        cb_count = combobox.count()

        message = 'Expected %s items in the combobox, but got %s' % (str(expected_count), str(cb_count))
        self.assertEqual(str(expected_count), str(cb_count), message)


if __name__ == "__main__":
    suite = unittest.makeSuite(GeosysPluginDockWidgetTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
