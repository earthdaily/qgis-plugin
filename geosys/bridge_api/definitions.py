# coding=utf-8
"""This module contains definitions used by Bridge API Interface.
"""

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

# Crop types definition
CROPS = {
    'corn': 'CORN',
    'cotton': 'COTTON',
    'grapes': 'GRAPES',
    'millet': 'MILLET',
    'orange': 'ORANGE',
    'others': 'OTHERS',
    'peanut': 'PEANUT',
    'rice': 'RICE',
    'sugarcane': 'SUGARCANE',
    'sunflower': 'SUNFLOWER',
    'sorghum': 'SORGHUM',
    'soybeans': 'SOYBEANS'
}

# Map type families definition
base_reference_map = {
    'key': 'base-reference-map',
    'endpoint': 'base-reference-map'
}
canopy_map = {
    'key': 'canopy-map',
    'endpoint': 'canopy-map'
}
canopy_osr_map = {
    'key': 'canopy-osr-map',
    'endpoint': 'canopy-osr-map'
}
difference_map = {
    'key': 'difference-map',
    'endpoint': 'difference-map'
}
management_zones_map = {
    'key': 'management-zones-map',
    'endpoint': 'management-zones-map'
}
model_map = {
    'key': 'model-map',
    'endpoint': 'model-map'
}
organic_matter_map = {
    'key': 'organic-matter-map',
    'endpoint': 'organic-matter-map'
}
topology_map = {
    'key': 'topology-map',
    'endpoint': 'topology-map'
}
yield_goal_map = {
    'key': 'yield-goal-map',
    'endpoint': 'yield-goal-map'
}
yield_variability_map = {
    'key': 'yield-variability-map',
    'endpoint': 'yield-variability-map'
}

# Map types definition

# NDVI (Normalized Difference Vegetation Index)
# https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
NDVI = {
    'key': 'NDVI',
    'name': 'NDVI',
    'map_family': base_reference_map
}
INSEASON_NDVI = {
    'key': 'INSEASON_NDVI',
    'name': 'INSEASON_NDVI',
    'map_family': base_reference_map
}
INSEASONPARTIAL_NDVI = {
    'key': 'INSEASON_PARTIAL_NDVI',
    'name': 'INSEASON_PARTIAL_NDVI',
    'map_family': base_reference_map
}
INSEASONFIELD_AVERAGE_NDVI = {
    'key': 'INSEASONFIELD_AVERAGE_NDVI',
    'name': 'INSEASONFIELD_AVERAGE_NDVI',
    'map_family': model_map
}
INSEASONFIELD_AVERAGE_REVERSE_NDVI = {
    'key': 'INSEASONFIELD_AVERAGE_REVERSE_NDVI',
    'name': 'INSEASONFIELD_AVERAGE_REVERSE_NDVI',
    'map_family': model_map
}

# EVI (Enhanced Vegetation Index)
# https://en.wikipedia.org/wiki/Enhanced_vegetation_index
EVI = {
    'key': 'EVI',
    'name': 'EVI',
    'map_family': base_reference_map
}
INSEASON_EVI = {
    'key': 'INSEASON_EVI',
    'name': 'INSEASON_EVI',
    'map_family': base_reference_map
}
INSEASONPARTIAL_EVI = {
    'key': 'INSEASONPARTIAL_EVI',
    'name': 'INSEASONPARTIAL_EVI',
    'map_family': base_reference_map
}

# CVI (Chlorophyll Vegetation Index)
CVI = {
    'key': 'CVI',
    'name': 'CVI',
    'map_family': base_reference_map
}
INSEASON_CVI = {
    'key': 'INSEASON_CVI',
    'name': 'INSEASON_CVI',
    'map_family': base_reference_map
}

# GNDVI (Green Normalized Difference Vegetation Index)
GNDVI = {
    'key': 'GNDVI',
    'name': 'GNDVI',
    'map_family': base_reference_map
}
INSEASON_GNDVI = {
    'key': 'INSEASON_GNDVI',
    'name': 'INSEASON_GNDVI',
    'map_family': base_reference_map
}

# LAI (Leaf Area Index)
INSEASON_LAI = {
    'key': 'INSEASON_LAI',
    'name': 'INSEASON_LAI',
    'map_family': base_reference_map
}
INSEASONCANOPY_N_REVERSE_LAI = {
    'key': 'INSEASONCANOPY_N_REVERSE_LAI',
    'name': 'INSEASONCANOPY_N_REVERSE_LAI',
    'map_family': model_map
}
INSEASONFIELD_AVERAGE_LAI = {
    'key': 'INSEASONFIELD_AVERAGE_LAI',
    'name': 'INSEASONFIELD_AVERAGE_LAI',
    'map_family': model_map
}
INSEASONFIELD_AVERAGE_REVERSE_LAI = {
    'key': 'INSEASONFIELD_AVERAGE_REVERSE_LAI',
    'name': 'INSEASONFIELD_AVERAGE_REVERSE_LAI',
    'map_family': model_map
}


# OM (Organic Matter)
OM = {
    'key': 'OM',
    'name': 'OM',
    'map_family': organic_matter_map
}

# YGM (Yield Goal Map)
YGM = {
    'key': 'YGM',
    'name': 'YGM',
    'map_family': yield_goal_map
}

# YVM (Yield Variability Map)
YVM = {
    'key': 'YPM',
    'name': 'YPM',
    'map_family': yield_variability_map
}

# SaMZ
SAMZ = {
    'key': 'SAMZ',
    'name': 'SAMZ',
    'map_family': management_zones_map
}

# Color Composition
COLOR_COMPOSITION = {
    'key': 'COLORCOMPOSITION',
    'name': 'COLORCOMPOSITION',
    'map_family': base_reference_map
}

# Topology
ELEVATION = {
    'key': 'ELEVATION',
    'name': 'ELEVATION',
    'map_family': topology_map
}
EROSION = {
    'key': 'EROSION',
    'name': 'EROSION',
    'map_family': topology_map
}
SLOPE = {
    'key': 'SLOPE',
    'name': 'SLOPE',
    'map_family': topology_map
}

# Difference map
DIFFERENCE_INSEASON_NDVI = {
    'key': 'DIFFERENCE_INSEASON_NDVI',
    'name': 'DIFFERENCE_INSEASON_NDVI',
    'map_family': difference_map
}
DIFFERENCE_INSEASON_EVI = {
    'key': 'DIFFERENCE_INSEASON_EVI',
    'name': 'DIFFERENCE_INSEASON_EVI',
    'map_family': difference_map
}

ARCHIVE_MAP_PRODUCTS = [
    INSEASON_NDVI,
    INSEASON_GNDVI,
    INSEASON_EVI,
    INSEASON_CVI,
    INSEASONPARTIAL_NDVI,
    INSEASONPARTIAL_EVI,
    COLOR_COMPOSITION,
    ELEVATION,
    OM,
    YGM,
    YVM,
    SAMZ,
    NDVI
]

INSEASON_MAP_PRODUCTS = [
    INSEASON_NDVI,
    INSEASONFIELD_AVERAGE_NDVI,
    INSEASONFIELD_AVERAGE_REVERSE_NDVI,
    INSEASON_CVI,
    INSEASON_EVI,
    INSEASONPARTIAL_NDVI,
    INSEASONPARTIAL_EVI,
    INSEASON_GNDVI,
    COLOR_COMPOSITION
]

DIFFERENCE_MAPS = [
    DIFFERENCE_INSEASON_NDVI,
    DIFFERENCE_INSEASON_EVI
]

# Sensor definition

DEIMOS = {
    'key': 'DEIMOS',
    'name': 'DEIMOS',
}

DMC = {
    'key': 'DMC',
    'name': 'DMC'
}

LANDSAT_8 = {
    'key': 'LANDSAT_8',
    'name': 'LANDSAT_8'
}

RESOURCESAT2 = {
    'key': 'RESOURCESAT2',
    'name': 'RESOURCESAT2'
}

SENTINEL_2 = {
    'key': 'SENTINEL_2',
    'name': 'SENTINEL_2'
}

SENSORS = [
    DEIMOS, DMC, LANDSAT_8, RESOURCESAT2, SENTINEL_2
]

ALL_SENSORS = {
    'key': 'ALL_SENSORS',
    'name': 'ALL SENSORS',
    'sensors': SENSORS
}
