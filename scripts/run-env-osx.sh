#!/bin/bash

#QGISPATH=`find /usr/local/ -name QGIS.app`
QGIS_PATH=/Applications/QGIS3.6.app
export QGIS_PREFIX_PATH=${QGIS_PATH}/Contents/MacOS
echo "QGIS PATH: $QGIS_PREFIX_PATH"
PYTHONPATH=$PYTHONPATH:${QGIS_PATH}/Contents/Resources/python
# Needed for importing processing plugin
PYTHONPATH=$PYTHONPATH:${QGIS_PATH}/Contents/Resources/python/plugins
export PYTHONPATH

export QGIS_DEBUG=0
export QGIS_LOG_FILE=/tmp/geosys/logs/qgis.log

echo "PYTHON PATH: $PYTHONPATH"
