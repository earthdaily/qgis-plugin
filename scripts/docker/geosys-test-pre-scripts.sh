#!/usr/bin/env bash

qgis_setup.sh

# FIX default installation because the sources must be in "stream_feature_extractor" parent folder
rm -rf  /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/stream_feature_extractor
ln -sf /tests_directory /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/stream_feature_extractor
ln -sf /tests_directory /usr/share/qgis/python/plugins/stream_feature_extractor

pip3 install -r /tests_directory/REQUIREMENTS.txt
pip3 install -r /tests_directory/REQUIREMENTS_TESTING.txt