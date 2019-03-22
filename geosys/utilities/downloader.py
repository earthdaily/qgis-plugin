# coding=utf-8
"""Helpers for QGIS related functionality."""
import os
import zipfile

from urllib2 import urlopen, HTTPError, URLError

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


def fetch_zip(url, output_path):
    """Download zip file and write it to output_path.

    :param url: URL of the zip bundle.
    :type url: str

    :param output_path: Path of the output file.
    :type output_path: str
    """
    # Download Process
    try:
        f = urlopen(url)
        # Open our local file for writing
        with open(output_path, "w") as local_file:
            local_file.write(f.read())

        # handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def extract_zip(zip_path, destination_base_path):
    """Extract different extensions to the destination base path.

    Example : test.zip contains a.shp, a.dbf, a.prj
    and destination_base_path = '/tmp/CT-buildings
    Expected result :
        - /tmp/CT-buildings.shp
        - /tmp/CT-buildings.dbf
        - /tmp/CT-buildings.prj

    If two files in the zip with the same extension, only one will be
    copied.

    :param zip_path: The path of the .zip file
    :type zip_path: str

    :param destination_base_path: The destination base path where the shp
        will be written to.
    :type destination_base_path: str

    :raises: IOError - when not able to open path or output_dir does not
        exist.
    """
    handle = open(zip_path, 'rb')
    zip_file = zipfile.ZipFile(handle)
    for name in zip_file.namelist():
        extension = os.path.splitext(name)[1]
        output_final_path = '%s%s' % (destination_base_path, extension)
        output_file = open(output_final_path, 'wb')
        output_file.write(zip_file.read(name))
        output_file.close()

    handle.close()
