# coding=utf-8
"""Helpers for QGIS related functionality."""
import logging
import os
import zipfile

from qgis.core import QgsApplication, QgsNetworkAccessManager
# noinspection PyPackageRequirements
from qgis.PyQt.QtCore import QByteArray, QFile, QUrl
# noinspection PyPackageRequirements
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

LOGGER = logging.getLogger('GEOSYS Plugin')


def fetch_zip(url, output_path, headers=None, progress_dialog=None):
    """Download zip containing shp file and write to output_path.

    :param url: URL of the zip bundle.
    :type url: str

    :param output_path: Path of output file,
    :type output_path: str

    :param headers: Request headers.
    :type headers: dict

    :param progress_dialog: A progress dialog.
    :type progress_dialog: QProgressDialog

    :raises: ImportDialogError - when network error occurred
    """
    LOGGER.debug('Downloading file from URL: %s' % url)
    LOGGER.debug('Downloading to: %s' % output_path)

    if progress_dialog:
        progress_dialog.show()

        # Infinite progress bar when the server is fetching data.
        # The progress bar will be updated with the file size later.
        progress_dialog.setMaximum(0)
        progress_dialog.setMinimum(0)
        progress_dialog.setValue(0)

        label_text = ('Fetching %s' % url)
        progress_dialog.setLabelText(label_text)

    # Download Process
    downloader = FileDownloader(url, output_path, headers, progress_dialog)
    try:
        result = downloader.download()
    except IOError as ex:
        raise IOError(ex)

    if result[0] is not True:
        _, error_message = result
        raise Exception(error_message)


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


class FileDownloader:
    """The blueprint for downloading file from url."""

    def __init__(self, url, output_path, headers=None, progress_dialog=None):
        """Constructor of the class.

        :param url: URL of file.
        :type url: str

        :param output_path: Output path.
        :type output_path: str

        :param progress_dialog: Progress dialog widget.
        :type progress_dialog: QWidget
        """
        # noinspection PyArgumentList
        self.manager = QgsNetworkAccessManager.instance()
        self.url = QUrl(url)
        self.output_path = output_path
        self.headers = headers if headers else {}
        self.progress_dialog = progress_dialog
        if self.progress_dialog:
            self.prefix_text = self.progress_dialog.labelText()
        self.output_file = None
        self.reply = None
        self.downloaded_file_buffer = None
        self.finished_flag = False

    def download(self):
        """Downloading the file.

        :returns: True if success, otherwise returns a tuple with format like
            this (QNetworkReply.NetworkError, error_message)

        :raises: IOError - when cannot create output_path
        """
        # Prepare output path
        self.output_file = QFile(self.output_path)
        if not self.output_file.open(QFile.WriteOnly):
            raise IOError(self.output_file.errorString())

        # Prepare downloaded buffer
        self.downloaded_file_buffer = QByteArray()

        # Request the url
        request = QNetworkRequest(self.url)
        # Set headers if any
        for header_name, header_value in self.headers.items():
            # For PyQt5 < 5.5 you could pass a python string
            # (i.e. text without an encoding) for a QByteArray.
            # Now you can't, because PyQt just guessed an encoding
            # which might be wrong.
            # http://pyqt.sourceforge.net/Docs/PyQt5/incompatibilities.html
            # Pass a bytes object instead, e.g. by adding a 'b' before
            # your string in your case:
            #   request.setRawHeader(b'user-agent', userAgent)
            request.setRawHeader(
                bytes(header_name, 'utf-8'), bytes(header_value, 'utf-8'))
        self.reply = self.manager.get(request)
        self.reply.readyRead.connect(self.get_buffer)
        self.reply.finished.connect(self.write_data)
        self.manager.requestTimedOut.connect(self.request_timeout)

        if self.progress_dialog:
            # progress bar
            def progress_event(received, total):
                """Update progress.

                :param received: Data received so far.
                :type received: int

                :param total: Total expected data.
                :type total: int
                """
                # noinspection PyArgumentList
                QgsApplication.processEvents()

                self.progress_dialog.adjustSize()

                label_text = (
                        "%s : %s of %s" % (self.prefix_text, received, total))

                self.progress_dialog.setLabelText(label_text)
                self.progress_dialog.setMaximum(total)
                self.progress_dialog.setValue(received)

            # cancel
            def cancel_action():
                """Cancel download."""
                self.reply.abort()
                self.reply.deleteLater()

            self.reply.downloadProgress.connect(progress_event)
            self.progress_dialog.canceled.connect(cancel_action)

        # Wait until finished
        # On Windows 32bit AND QGIS 2.2, self.reply.isFinished() always
        # returns False even after finished slot is called. So, that's why we
        # are adding self.finished_flag (see #864)
        while not self.reply.isFinished() and not self.finished_flag:
            # noinspection PyArgumentList
            QgsApplication.processEvents()

        result = self.reply.error()
        try:
            http_code = int(self.reply.attribute(
                QNetworkRequest.HttpStatusCodeAttribute))
        except TypeError:
            # If the user cancels the request, the HTTP response will be None.
            http_code = None

        self.reply.abort()
        self.reply.deleteLater()

        if result == QNetworkReply.NoError:
            return True, None

        elif result == QNetworkReply.UnknownNetworkError:
            return False, (
                'The network is unreachable. Please check your internet '
                'connection.')

        elif http_code == 408:
            msg = (
                'Sorry, the server aborted your request. '
                'Please try a smaller area.')
            LOGGER.debug(msg)
            return False, msg

        elif http_code == 509:
            msg = (
                'Sorry, the server is currently busy with another request. '
                'Please try again in a few minutes.')
            LOGGER.debug(msg)
            return False, msg

        elif result == QNetworkReply.ProtocolUnknownError or \
                result == QNetworkReply.HostNotFoundError:
            # See http://doc.qt.io/qt-5/qurl-obsolete.html#encodedHost
            encoded_host = self.url.toAce(self.url.host())
            LOGGER.exception('Host not found : %s' % encoded_host)
            return False, (
                'Sorry, the server is unreachable. Please try again later.')

        elif result == QNetworkReply.ContentNotFoundError:
            LOGGER.exception('Path not found : %s' % self.url.path())
            return False, 'Sorry, the content was not found on the server.'

        else:
            return result, self.reply.errorString()

    def get_buffer(self):
        """Get buffer from self.reply and store it to our buffer container."""
        buffer_size = self.reply.size()
        data = self.reply.read(buffer_size)
        self.downloaded_file_buffer.append(data)

    def write_data(self):
        """Write data to a file."""
        self.output_file.write(self.downloaded_file_buffer)
        self.output_file.close()
        self.finished_flag = True

    def request_timeout(self):
        """The request timed out."""
        if self.progress_dialog:
            self.progress_dialog.hide()
