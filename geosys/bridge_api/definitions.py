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
    'key': 'ndvi',
    'name': 'NDVI',
    'map_family': base_reference_map
}
INSEASON_NDVI = {
    'key': 'inseason-ndvi',
    'name': 'INSEASON_NDVI',
    'map_family': base_reference_map
}
INSEASONPARTIAL_NDVI = {
    'key': 'inseason-partial-ndvi',
    'name': 'INSEASON_PARTIAL_NDVI',
    'map_family': base_reference_map
}
INSEASONFIELD_AVERAGE_NDVI = {
    'key': 'inseason-field-average-ndvi',
    'name': 'INSEASONFIELD_AVERAGE_NDVI',
    'map_family': model_map
}
INSEASONFIELD_AVERAGE_REVERSE_NDVI = {
    'key': 'inseason-field-average-reverse-ndvi',
    'name': 'INSEASONFIELD_AVERAGE_REVERSE_NDVI',
    'map_family': model_map
}

# EVI (Enhanced Vegetation Index)
# https://en.wikipedia.org/wiki/Enhanced_vegetation_index
EVI = {
    'key': 'evi',
    'name': 'EVI',
    'map_family': base_reference_map
}
INSEASON_EVI = {
    'key': 'inseason-evi',
    'name': 'INSEASON_EVI',
    'map_family': base_reference_map
}
INSEASONPARTIAL_EVI = {
    'key': 'inseason-partial-evi',
    'name': 'INSEASONPARTIAL_EVI',
    'map_family': base_reference_map
}

# CVI (Chlorophyll Vegetation Index)
CVI = {
    'key': 'cvi',
    'name': 'CVI',
    'map_family': base_reference_map
}
INSEASON_CVI = {
    'key': 'inseason-cvi',
    'name': 'INSEASON_CVI',
    'map_family': base_reference_map
}

# GNDVI (Green Normalized Difference Vegetation Index)
GNDVI = {
    'key': 'gndvi',
    'name': 'GNDVI',
    'map_family': base_reference_map
}
INSEASON_GNDVI = {
    'key': 'inseason-gndvi',
    'name': 'INSEASON_GNDVI',
    'map_family': base_reference_map
}

# LAI (Leaf Area Index)
INSEASON_LAI = {
    'key': 'inseason-lai',
    'name': 'INSEASON_LAI',
    'map_family': base_reference_map
}
INSEASONCANOPY_N_REVERSE_LAI = {
    'key': 'inseasoncanopy-n-reverse-lai',
    'name': 'INSEASONCANOPY_N_REVERSE_LAI',
    'map_family': model_map
}
INSEASONFIELD_AVERAGE_LAI = {
    'key': 'inseasonfield-average-lai',
    'name': 'INSEASONFIELD_AVERAGE_LAI',
    'map_family': model_map
}
INSEASONFIELD_AVERAGE_REVERSE_LAI = {
    'key': 'inseasonfield-average-reverse-lai',
    'name': 'INSEASONFIELD_AVERAGE_REVERSE_LAI',
    'map_family': model_map
}


# OM (Organic Matter)
OM = {
    'key': 'om',
    'name': 'OM',
    'map_family': organic_matter_map
}

# YGM (Yield Goal Map)
YGM = {
    'key': 'ygm',
    'name': 'YGM',
    'map_family': yield_goal_map
}

# YVM (Yield Variability Map)
YVM = {
    'key': 'yvm',
    'name': 'YPM',
    'map_family': yield_variability_map
}

# SaMZ
SAMZ = {
    'key': 'samz',
    'name': 'SAMZ',
    'map_family': management_zones_map
}

# Color Composition
COLOR_COMPOSITION = {
    'key': 'color-composition',
    'name': 'COLORCOMPOSITION',
    'map_family': base_reference_map
}

# Topology
ELEVATION = {
    'key': 'elevation',
    'name': 'ELEVATION',
    'map_family': topology_map
}
EROSION = {
    'key': 'erosion',
    'name': 'EROSION',
    'map_family': topology_map
}
SLOPE = {
    'key': 'slope',
    'name': 'SLOPE',
    'map_family': topology_map
}
