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
soil_map = {
    'key': 'soilmap',
    'endpoint': 'soilmap'
}
reflectance_map = {
    'key': 'reflectance-map',
    'endpoint': 'reflectance-map'
}

# Map types definition

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

# NDVI (Normalized Difference Vegetation Index)
# https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
INSEASON_NDVI = {
    'key': 'INSEASON_NDVI',
    'name': 'INSEASON_NDVI',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Normalized Difference '
                   'Vegetation Index.',
    'difference_map': DIFFERENCE_INSEASON_NDVI
}
INSEASONPARTIAL_NDVI = {
    'key': 'INSEASONPARTIAL_NDVI',
    'name': 'INSEASONPARTIAL_NDVI',
    'map_family': base_reference_map,
    'description': 'Provides the partial Normalized Difference '
                   'Vegetation Index.'
}
INSEASONFIELD_AVERAGE_NDVI = {
    'key': 'INSEASONFIELD_AVERAGE_NDVI',
    'name': 'INSEASONFIELD_AVERAGE_NDVI',
    'map_family': model_map,
    'description': ''
}
INSEASONFIELD_AVERAGE_REVERSE_NDVI = {
    'key': 'INSEASONFIELD_AVERAGE_REVERSE_NDVI',
    'name': 'INSEASONFIELD_AVERAGE_REVERSE_NDVI',
    'map_family': model_map,
    'description': ''
}

# EVI (Enhanced Vegetation Index)
# https://en.wikipedia.org/wiki/Enhanced_vegetation_index
EVI = {
    'key': 'EVI',
    'name': 'EVI',
    'map_family': base_reference_map,
    'description': ''
}
INSEASON_EVI = {
    'key': 'INSEASON_EVI',
    'name': 'INSEASON_EVI',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Enhanced Vegetation Index.',
    'difference_map': DIFFERENCE_INSEASON_EVI
}
INSEASONPARTIAL_EVI = {
    'key': 'INSEASONPARTIAL_EVI',
    'name': 'INSEASONPARTIAL_EVI',
    'map_family': base_reference_map,
    'description': 'Provides the partial Enhanced Vegetation Index.'
}

# CVI (Chlorophyll Vegetation Index)
CVI = {
    'key': 'CVI',
    'name': 'CVI',
    'map_family': base_reference_map,
    'description': ''
}
INSEASON_CVI = {
    'key': 'INSEASON_CVI',
    'name': 'INSEASON_CVI',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Chlorophyll Vegetation Index. '
                   'It is used as an indicator of photosynthetic energy '
                   'conversion.'
}

# GNDVI (Green Normalized Difference Vegetation Index)
GNDVI = {
    'key': 'GNDVI',
    'name': 'GNDVI',
    'map_family': base_reference_map,
    'description': ''
}
INSEASON_GNDVI = {
    'key': 'INSEASON_GNDVI',
    'name': 'INSEASON_GNDVI',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Green Normalized Difference '
                   'Vegetation Index.'
}

# LAI (Leaf Area Index)
INSEASON_LAI = {
    'key': 'INSEASON_LAI',
    'name': 'INSEASON_LAI',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Leave Area Index. '
                   'The LAI is a dimensionless ranging from 0 (bare ground) '
                   'to over 10 (dense conifer forests).'
}
INSEASONCANOPY_N_REVERSE_LAI = {
    'key': 'INSEASONCANOPY_N_REVERSE_LAI',
    'name': 'INSEASONCANOPY_N_REVERSE_LAI',
    'map_family': model_map,
    'description': ''
}
INSEASONFIELD_AVERAGE_LAI = {
    'key': 'INSEASONFIELD_AVERAGE_LAI',
    'name': 'INSEASONFIELD_AVERAGE_LAI',
    'map_family': model_map,
    'description': ''
}
INSEASONFIELD_AVERAGE_REVERSE_LAI = {
    'key': 'INSEASONFIELD_AVERAGE_REVERSE_LAI',
    'name': 'INSEASONFIELD_AVERAGE_REVERSE_LAI',
    'map_family': model_map,
    'description': ''
}

# Sentinel-2 Red-edge position index (S2REP)
INSEASON_S2REP = {
    'key': 'INSEASON_S2REP',
    'name': 'INSEASON_S2REP',
    'map_family': base_reference_map,
    'description': 'Provides the in-season S2REP index. '
                   'Generates a map according to the amount '
                   'of chlorophyll content per unit of leaf (LCC).'
}

# Chlorophyll vegetation index
INSEASON_CVIN = {
    'key': 'INSEASON_CVIN',
    'name': 'INSEASON_CVIN',
    'map_family': base_reference_map,
    'description': 'Provides the in-season Chlorophyll Vegetation Index normalized.'
}

# Soil
SOIL = {
    'key': 'SOIL',
    'name': 'SOIL',
    'map_family': soil_map,
    'description': 'Provides the in-season Soil type map. '
                   'Can be generated only in the USA, contains '
                   'information about soil as collected by the '
                   'National Cooperative Soil Survey.'
}

# Reflectance
REFLECTANCE = {
    'key': 'REFLECTANCE',
    'name': 'REFLECTANCE',
    'map_family': reflectance_map,
    'description': 'Provides the reflectance at Top of Canopy for Sentinel 2 and Landsat-8.'
}

# OM (Organic Matter)
OM = {
    'key': 'OM',
    'name': 'OM',
    'map_family': organic_matter_map,
    'description': 'Provides the Organic Matter map.'
}

# YGM (Yield Goal Map)
YGM = {
    'key': 'YGM',
    'name': 'YGM',
    'map_family': yield_goal_map,
    'description': 'Provides the Yield Goal Map.'
}

# YVM (Yield Variability Map)
YVM = {
    'key': 'YPM',
    'name': 'YPM',
    'map_family': yield_variability_map,
    'description': 'Provides the Yield Variability Map.'
}

# SaMZ
SAMZ = {
    'key': 'SAMZ',
    'name': 'SAMZ',
    'map_family': management_zones_map,
    'description': 'Provides the management zones map.'
}

# Color Composition
COLOR_COMPOSITION = {
    'key': 'COLORCOMPOSITION',
    'name': 'COLORCOMPOSITION',
    'map_family': base_reference_map,
    'description': 'Provides the color composition map.'
}

# Topology
ELEVATION = {
    'key': 'ELEVATION',
    'name': 'ELEVATION',
    'map_family': topology_map,
    'description': 'Provides the elevation map.'
}
EROSION = {
    'key': 'EROSION',
    'name': 'EROSION',
    'map_family': topology_map,
    'description': 'Provides the erosion map.'
}
SLOPE = {
    'key': 'SLOPE',
    'name': 'SLOPE',
    'map_family': topology_map,
    'description': 'Provides the slope map.'
}

ARCHIVE_MAP_PRODUCTS = [
    INSEASON_NDVI,
    INSEASON_GNDVI,
    INSEASON_EVI,
    INSEASON_CVI,
    INSEASONPARTIAL_NDVI,
    INSEASONPARTIAL_EVI,
    INSEASON_LAI,
    INSEASONFIELD_AVERAGE_NDVI,
    INSEASONFIELD_AVERAGE_LAI,
    INSEASONFIELD_AVERAGE_REVERSE_NDVI,
    INSEASONFIELD_AVERAGE_REVERSE_LAI,
    INSEASON_S2REP,
    INSEASON_CVIN,
    COLOR_COMPOSITION,
    ELEVATION,
    OM,
    YGM,
    YVM,
    SAMZ,
    SOIL,
    REFLECTANCE
]

BASIC_INSEASON_MAP_PRODUCTS = [
    INSEASON_NDVI,
    INSEASON_EVI,
    INSEASON_CVI,
    INSEASON_GNDVI,
    INSEASON_LAI,
    INSEASON_S2REP
]

INSEASON_MAP_PRODUCTS = BASIC_INSEASON_MAP_PRODUCTS + [
    INSEASONFIELD_AVERAGE_NDVI,
    INSEASONFIELD_AVERAGE_REVERSE_NDVI,
    INSEASONFIELD_AVERAGE_LAI,
    INSEASONFIELD_AVERAGE_REVERSE_LAI,
    INSEASONPARTIAL_NDVI,
    INSEASONPARTIAL_EVI,
]

DIFFERENCE_MAPS = [
    DIFFERENCE_INSEASON_NDVI,
    DIFFERENCE_INSEASON_EVI
]

# Sensor definition

DEIMOS = {
    'key': 'DEIMOS',
    'name': 'DEIMOS',
    'description': 'Commercial data at 0.75 metre resolution.'
}

DMC = {
    'key': 'DMC',
    'name': 'DMC',
    'description': 'Images comparable to Landsat in resolution but with '
                   'higher image intervals.'
}

LANDSAT_8 = {
    'key': 'LANDSAT_8',
    'name': 'LANDSAT_8',
    'description': 'Providing moderate-resolution imagery at 30 meters '
                   'resampled to 15 meters by Geosys. Revisiting every '
                   '16 days.'
}

RESOURCESAT2 = {
    'key': 'RESOURCESAT2',
    'name': 'RESOURCESAT2',
    'description': 'The Linear Imaging Self-Scanning Sensor (LISS-III) '
                   'with 23.5 meter spatial resolution LISS-IV Camera with '
                   '5.8 meter spatial resolution. '
                   'Revisiting every 24 days.'
}

SENTINEL_2 = {
    'key': 'SENTINEL_2',
    'name': 'SENTINEL_2',
    'description': 'Spatial resolution of 10 m, 20 m and 60 m. '
                   'Revisiting every 5 days under the same viewing angles. '
                   'At high latitudes, Sentinel-2 swath overlap and some '
                   'regions will be observed twice or more every 5 days, '
                   'but with different viewing angles. Multi-spectral data '
                   'with 13 bands in the visible, near infrared, and short '
                   'wave infrared part of the spectrum.'
}

SENSORS = [
    DEIMOS, DMC, LANDSAT_8, RESOURCESAT2, SENTINEL_2
]

ALL_SENSORS = {
    'key': 'ALL_SENSORS',
    'name': 'ALL SENSORS',
    'sensors': SENSORS
}
