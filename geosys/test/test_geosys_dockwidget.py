# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'andre@kartoza.com'
__date__ = '2019-03-11'
__copyright__ = 'Copyright 2019, Kartoza'

import unittest

from geosys.test.test_resources import GeosysPluginDialogTest
from geosys.test.utilities import get_qgis_app
from geosys.ui.widgets.geosys_dockwidget import GeosysPluginDockWidget

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

if __name__ == "__main__":
    suite = unittest.makeSuite(GeosysPluginDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

