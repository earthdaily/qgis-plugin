# coding=utf-8
"""GUI utilities for the dock and the multi Exposure Tool."""
import os
from past.builtins import cmp

from qgis.core import (
    QgsProject,
    QgsMapLayer,
    QgsLayerItem,
    QgsWkbTypes,
    QgsCoordinateTransform,
    QgsFeature,
    QgsMemoryProviderUtils,
    QgsFields,
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsVectorFileWriter)

from qgis.PyQt.QtCore import Qt
from PyQt5.QtCore import QVariant

from geosys.utilities.qgis import qgis_version
from geosys.bridge_api.default import SHP_EXT
from geosys.utilities.settings import setting

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


def item_data_from_combo(combo):
    """Get the item data currently selected in a combo box.

    :returns: The currently selected combo box item data.
    :rtype: any
    """
    index = combo.currentIndex()
    if index < 0:
        return None

    item_data = combo.itemData(index, Qt.UserRole)
    return item_data


def item_text_from_combo(combo):
    """Get the item text currently selected in a combo box.
    :returns: The currently selected combo box item text.
    :rtype: str
    """
    index = combo.currentIndex()

    if index < 0:
        return None

    item_data = combo.itemText(index)
    return item_data


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


def create_memory_layer(
        layer_name, geometry, coordinate_reference_system=None, fields=None):
    """Create a vector memory layer.

    :param layer_name: The name of the layer.
    :type layer_name: str

    :param geometry: The geometry of the layer.
    :rtype geometry: QgsWkbTypes (note:
                     from C++ QgsWkbTypes::GeometryType enum)

    :param coordinate_reference_system: The CRS of the memory layer.
    :type coordinate_reference_system: QgsCoordinateReferenceSystem

    :param fields: Fields of the vector layer. Default to None.
    :type fields: QgsFields

    :return: The memory layer.
    :rtype: QgsVectorLayer
    """

    if geometry == QgsWkbTypes.PointGeometry:
        wkb_type = QgsWkbTypes.MultiPoint
    elif geometry == QgsWkbTypes.LineGeometry:
        wkb_type = QgsWkbTypes.MultiLineString
    elif geometry == QgsWkbTypes.PolygonGeometry:
        wkb_type = QgsWkbTypes.MultiPolygon
    elif geometry == QgsWkbTypes.NullGeometry:
        wkb_type = QgsWkbTypes.NoGeometry
    else:
        raise Exception(
            'Layer geometry must be one of: Point, Line, '
            'Polygon or Null, I got %s' % geometry)

    if coordinate_reference_system is None:
        coordinate_reference_system = QgsCoordinateReferenceSystem()
    if fields is None:
        fields = QgsFields()
    elif not isinstance(fields, QgsFields):
        # fields is a list
        new_fields = QgsFields()
        for f in fields:
            new_fields.append(f)
        fields = new_fields
    memory_layer = QgsMemoryProviderUtils. \
        createMemoryLayer(name=layer_name,
                          fields=fields,
                          geometryType=wkb_type,
                          crs=coordinate_reference_system)

    memory_layer.dataProvider().createSpatialIndex()
    return memory_layer


def reproject(layer, output_crs):
    """Reproject a vector layer to a specific CRS.

    :param layer: The layer to reproject.
    :type layer: QgsVectorLayer

    :param output_crs: The destination CRS.
    :type output_crs: QgsCoordinateReferenceSystem

    :return: Reprojected memory layer.
    :rtype: QgsVectorLayer
    """
    output_layer_name = '{}_reprojected'.format(layer.name())

    input_crs = layer.crs()
    input_fields = layer.fields()

    reprojected = create_memory_layer(
        output_layer_name, layer.geometryType(), output_crs, input_fields)
    reprojected.startEditing()

    crs_transform = QgsCoordinateTransform(
        input_crs, output_crs, QgsProject.instance())

    out_feature = QgsFeature()

    for i, feature in enumerate(layer.getFeatures()):
        geom = feature.geometry()
        geom.transform(crs_transform)
        out_feature.setGeometry(geom)
        out_feature.setAttributes(feature.attributes())
        reprojected.addFeature(out_feature)

    reprojected.commitChanges()
    return reprojected


def wkt_geometries_from_feature_iterator(
        feature_iterator, max_features=None, as_single_geometry=False):
    """Get list of wkt geometries from a QgsMapLayer feature iterator.

    :param feature_iterator: QGIS layer feature iterator.
        *retrieved from QgsMapLayer.getFeatures()
    :type feature_iterator: QgsFeatureIterator

    :param max_features: Number of maximum features iteration.
    :type max_features: int

    :param as_single_geometry: Flag indicating whether to squash the features
        into single geometry or not.
    :type as_single_geometry: bool

    :return: List of wkt geometries.
    :rtype: list
    """
    geom = None
    geoms = []
    for index, feature in enumerate(feature_iterator):
        if index >= max_features:
            break
        if not feature.hasGeometry():
            continue
        if as_single_geometry:
            if not geom:
                geom = feature.geometry()
            else:
                geom = geom.combine(feature.geometry())
        else:
            geoms.append(feature.geometry())

    if geom:
        return [geom.asWkt()]
    elif geoms:
        return [geom.asWkt() for geom in geoms]
    else:
        return []


def create_hotspot_layer(source, source_type, source_filename):
    """Creates layer from wkt text in the source.

        :param source: Array with json objects containing WKT text.
        :type source: array
            example
            "source = [{
                "geometry": "POINT (-100.26517713 38.99869576)",
                "segmentId": 1
            },
            {
                "geometry": "POINT (-100.26977919 38.99869091)",
                "segmentId": 2
            }]
            or
            source = [
            {
                id: 1,
                segments:{
                  "id": 3,
                  "geometry": "POLYGON ((
                  -107.07693518495601 36.83928234462352,
                  -107.04672278261226 36.83928234462352,
                  -107.04672278261226 36.82169515605545,
                  -107.07693518495601 36.82169515605545,
                  -107.07693518495601 36.83928234462352))",
                  "stats": {
                    "mean": 76.566032409667969,
                    "max": 95.4800033569336,
                    "min": 68.2699966430664,
                    "area": 20200.183288909735,
                    "std": 6.545262336730957
                  }
                }
            }
            ]"

        :param source_type: Source type
        :type source_type: string

        :param source_filename: Filename of the result layer
        :type source_filename: string
    """
    crs = QgsCoordinateReferenceSystem()
    fields = QgsFields()
    features = []

    if source_type == "hotspots":
        layer_type = "MULTIPOINT?crs={}".format(crs.authid())
        fields.append(QgsField("segmentId", QVariant.String))

        for spot in source:
            geom = QgsGeometry.fromWkt(spot['geometry'])
            feature = QgsFeature()
            feature.setFields(fields)
            feature.setGeometry(geom)
            feature[0] = spot['segmentId']
            features.append(feature)
    else:
        layer_type = "MULTIPOLYGON?crs={}".format(crs.authid())
        for zone in source:
            fields.append(QgsField("id", QVariant.Int))
            fields.append(QgsField("mean", QVariant.Double))
            fields.append(QgsField("max", QVariant.Double))
            fields.append(QgsField("min", QVariant.Double))
            fields.append(QgsField("area", QVariant.Double))
            fields.append(QgsField("std", QVariant.Double))

            for polygon in zone.get('segments'):
                geom = QgsGeometry.fromWkt(polygon['geometry'])
                feature = QgsFeature()
                feature.setFields(fields)
                feature.setGeometry(geom)
                feature[0] = int(polygon['id'])
                feature[1] = float(polygon['stats']['mean'])
                feature[2] = float(polygon['stats']['max'])
                feature[3] = float(polygon['stats']['min'])
                feature[4] = float(polygon['stats']['area'])

                # The API produces None values for standard deviation
                # This check will leave the standard deviation as None in the attribute table if the response from the API is None
                # Otherwise the value from the API will be used
                std_value = polygon['stats']['std']
                if std_value is not None:
                    feature[5] = float(polygon['stats']['std'])

                features.append(feature)

    layer = QgsVectorLayer(layer_type, source_filename, "memory")
    layer.dataProvider().addAttributes(fields)
    layer.dataProvider().addFeatures(features)
    layer.updateExtents()
    layer.reload()

    file_name = '{}{}'.format(source_filename, SHP_EXT)
    output_dir = setting(
            'output_directory', expected_type=str)
    file_name = os.path.join(output_dir, file_name)

    # Save memory layer to disk
    error, error_message = QgsVectorFileWriter.writeAsVectorFormat(
        layer,
        file_name,
        "UTF-8",
        crs,
        "ESRI Shapefile")

    if error == QgsVectorFileWriter.NoError:
        saved_layer = QgsVectorLayer(file_name, source_filename, "ogr")
        add_layer_to_canvas(saved_layer, source_filename)
