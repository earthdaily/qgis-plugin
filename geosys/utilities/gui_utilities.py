# coding=utf-8
"""GUI utilities for the dock and the multi Exposure Tool."""
from past.builtins import cmp

from qgis.core import QgsProject, QgsMapLayer, QgsLayerItem, QgsWkbTypes
from qgis.PyQt.QtCore import Qt

from geosys.utilities.qgis import qgis_version

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


def layer_from_combo(combo):
    """Get the QgsMapLayer currently selected in a combo.

    Obtain QgsMapLayer id from the userrole of the QtCombo and return it as a
    QgsMapLayer.

    :returns: The currently selected map layer a combo.
    :rtype: QgsMapLayer
    """
    index = combo.currentIndex()
    if index < 0:
        return None

    layer_id = combo.itemData(index, Qt.UserRole)
    layer = QgsProject.instance().mapLayer(layer_id)
    return layer


def add_ordered_combo_item(
        combo, text, data=None, count_selected_features=None, icon=None):
    """Add a combo item ensuring that all items are listed alphabetically.

    Although QComboBox allows you to set an InsertAlphabetically enum
    this only has effect when a user interactively adds combo items to
    an editable combo. This we have this little function to ensure that
    combos are always sorted alphabetically.

    :param combo: Combo box receiving the new item.
    :type combo: QComboBox

    :param text: Display text for the combo.
    :type text: str

    :param data: Optional UserRole data to be associated with the item.
    :type data: QVariant, str

    :param count_selected_features: A count to display if the layer has some
    selected features. Default to None, nothing will be displayed.
    :type count_selected_features: None, int

    :param icon: Icon to display in the combobox.
    :type icon: QIcon
    """
    if count_selected_features is not None:
        text += ' (' + '{count} selected features'.format(
            count=count_selected_features) + ')'
    size = combo.count()
    for combo_index in range(0, size):
        item_text = combo.itemText(combo_index)
        # see if text alphabetically precedes item_text
        if cmp(text.lower(), item_text.lower()) < 0:
            if icon:
                combo.insertItem(combo_index, icon, text, data)
            else:
                combo.insertItem(combo_index, text, data)
            return

    # otherwise just add it to the end
    if icon:
        combo.insertItem(size, icon, text, data)
    else:
        combo.insertItem(size, text, data)


def is_raster_layer(layer):
    """Check if an object is QGIS raster layer.

    :param layer: A layer.
    :type layer: QgsRaster, QgsMapLayer, QgsVectorLayer

    :returns: True if the layer contains polygons, otherwise False.
    :rtype: bool
    """
    try:
        return layer.type() == QgsMapLayer.RasterLayer
    except AttributeError:
        return False


def is_vector_layer(layer):
    """Check if an object is QGIS vector layer.

    :param layer: A vector layer.
    :type layer: QgsVectorLayer, QgsMapLayer

    :returns: True if the layer is vector layer, otherwise False.
    :rtype: bool
    """
    try:
        return layer.type() == QgsMapLayer.VectorLayer
    except AttributeError:
        return False


def is_point_layer(layer):
    """Check if a QGIS layer is vector and its geometries are points.

    :param layer: A vector layer.
    :type layer: QgsVectorLayer, QgsMapLayer

    :returns: True if the layer contains points, otherwise False.
    :rtype: bool
    """
    try:
        return (layer.type() == QgsMapLayer.VectorLayer) and (
            layer.geometryType() == QgsWkbTypes.PointGeometry)
    except AttributeError:
        return False


def is_line_layer(layer):
    """Check if a QGIS layer is vector and its geometries are lines.

    :param layer: A vector layer.
    :type layer: QgsVectorLayer, QgsMapLayer

    :returns: True if the layer contains lines, otherwise False.
    :rtype: bool

    """
    try:
        return (layer.type() == QgsMapLayer.VectorLayer) and (
            layer.geometryType() == QgsWkbTypes.LineGeometry)
    except AttributeError:
        return False


def is_polygon_layer(layer):
    """Check if a QGIS layer is vector and its geometries are polygons.

    :param layer: A vector layer.
    :type layer: QgsVectorLayer, QgsMapLayer

    :returns: True if the layer contains polygons, otherwise False.
    :rtype: bool

    """
    try:
        return (layer.type() == QgsMapLayer.VectorLayer) and (
            layer.geometryType() == QgsWkbTypes.PolygonGeometry)
    except AttributeError:
        return False


def layer_icon(layer):
    """Helper to get the layer icon.

    :param layer: A layer.
    :type layer: QgsMapLayer

    :returns: The icon for the given layer.
    :rtype: QIcon
    """
    if is_raster_layer(layer):
        return QgsLayerItem.iconRaster()
    elif is_point_layer(layer):
        return QgsLayerItem.iconPoint()
    elif is_line_layer(layer):
        return QgsLayerItem.iconLine()
    elif is_polygon_layer(layer):
        return QgsLayerItem.iconPolygon()
    else:
        return QgsLayerItem.iconDefault()


def add_layer_to_canvas(layer, name):
    """Helper method to add layer to QGIS.

    :param layer: The layer.
    :type layer: QgsMapLayer

    :param name: Layer name.
    :type name: str

    """
    if qgis_version() >= 21800:
        layer.setName(name)
    else:
        layer.setLayerName(name)

    QgsProject.instance().addMapLayer(layer)
