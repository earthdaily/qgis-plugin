# coding=utf-8

"""Utilities module."""


import codecs
import json
import logging
import platform
import re
import os
import sys
import tempfile
import traceback
import unicodedata
import webbrowser

from geosys import messaging as m
from geosys.messaging import styles, Message
from geosys.messaging.error_message import ErrorMessage
from geosys.utilities.i18n import tr

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = '$Format:%H$'

INFO_STYLE = styles.BLUE_LEVEL_4_STYLE

LOGGER = logging.getLogger('geosys')


def basestring_to_message(text):
    """Convert a basestring to a Message object if needed.

    Avoid using this function, better to create the Message object yourself.
    This one is very generic.

    This function exists ust in case we get a basestring and we really need a
    Message object.

    :param text: The text.
    :type text: basestring, Message

    :return: The message object.
    :rtype: message
    """
    if isinstance(text, Message):
        return text
    elif text is None:
        return ''
    else:
        report = m.Message()
        report.add(text)
        return report


def get_error_message(exception, context=None, suggestion=None):
    """Convert exception into an ErrorMessage containing a stack trace.

    :param exception: Exception object.
    :type exception: Exception

    :param context: Optional context message.
    :type context: str

    :param suggestion: Optional suggestion.
    :type suggestion: str

    .. see also:: https://github.com/inasafe/inasafe/issues/577

    :returns: An error message with stack trace info suitable for display.
    :rtype: ErrorMessage
    """

    name, trace = humanise_exception(exception)

    problem = m.Message(name)

    if exception is None or exception == '':
        problem.append = m.Text(tr('No details provided'))
    else:
        if hasattr(exception, 'message') and \
                isinstance(exception.message, Message):
            problem.append = m.Text(str(exception.message.message))
        else:
            problem.append = m.Text(str(exception))

    suggestion = suggestion
    if suggestion is None and hasattr(exception, 'suggestion'):
        suggestion = exception.suggestion

    error_message = ErrorMessage(
        problem,
        detail=context,
        suggestion=suggestion,
        traceback=trace
    )

    args = exception.args
    for arg in args:
        error_message.details.append(arg)

    return error_message


def humanise_exception(exception):
    """Humanise a python exception by giving the class name and traceback.

    The function will return a tuple with the exception name and the traceback.

    :param exception: Exception object.
    :type exception: Exception

    :return: A tuple with the exception name and the traceback.
    :rtype: (str, str)
    """
    trace = ''.join(traceback.format_tb(sys.exc_info()[2]))
    name = exception.__class__.__name__
    return name, trace


def generate_expression_help(description, examples, extra_information=None):
    """Generate the help message for QGIS Expressions.

    It will format nicely the help string with some examples.

    :param description: A description of the expression.
    :type description: basestring

    :param examples: A dictionary of examples
    :type examples: dict

    :param extra_information: A dictionary of extra information.
    :type extra_information: dict

    :return: A message object.
    :rtype: message
    """
    def populate_bullet_list(message, information):
        """Populate a message object with bullet list.

        :param message: The message object.
        :type message: Message

        :param information: A dictionary of information.
        :type information: dict

        :return: A message object that has been updated.
        :rtype: Message
        """
        bullets = m.BulletedList()
        for key, item in list(information.items()):
            if item:
                bullets.add(
                    m.Text(m.ImportantText(key), m.Text('→'), m.Text(item)))
            else:
                bullets.add(m.Text(m.ImportantText(key)))
        message.add(bullets)
        return message

    help = m.Message()
    help.add(m.Paragraph(description))
    help.add(m.Paragraph(tr('Examples:')))
    help = populate_bullet_list(help, examples)

    if extra_information:
        help.add(m.Paragraph(extra_information['title']))
        help = populate_bullet_list(help, extra_information['detail'])

    return help


def open_in_browser(file_path):
    """Open a file in the default web browser.

    :param file_path: Path to the file that should be opened.
    :type file_path: str
    """
    webbrowser.open('file://%s' % file_path)


def html_to_file(html, file_path=None, open_browser=False):
    """Save the html to an html file adapting the paths to the filesystem.

    if a file_path is passed, it is used, if not a unique_filename is
    generated.

    :param html: the html for the output file.
    :type html: str

    :param file_path: the path for the html output file.
    :type file_path: str

    :param open_browser: if true open the generated html in an external browser
    :type open_browser: bool
    """
    if file_path is None:
        file_path = tempfile.mktemp(suffix='.html')

    # Ensure html is in unicode for codecs module
    html = html
    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    if open_browser:
        open_in_browser(file_path)


def replace_accentuated_characters(message):
    """Normalize unicode data in Python to remove umlauts, accents etc.

    :param message: The string where to delete accentuated characters.
    :type message: str, unicode

    :return: A string without umlauts, accents etc.
    :rtype: str
    """

    message = unicodedata.normalize('NFKD', message).encode('ASCII', 'ignore')
    return message.decode('utf-8')


def write_json(data, filename):
    """Custom handler for writing json file.

    Criteria:
    - use indent = 2
    - Handle NULL from QGIS

    :param data: The data that will be written.
    :type data: dict

    :param filename: The file name.
    :type filename: str
    """

    def custom_default(obj):
        if obj is None or (hasattr(obj, 'isNull') and obj.isNull()):
            return ''
        raise TypeError

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2, default=custom_default)


def human_sorting(the_list):
    """Sort the given list in the way that humans expect.

    From http://stackoverflow.com/a/4623518

    :param the_list: The list to sort.
    :type the_list: list

    :return: The new sorted list.
    :rtype: list
    """
    def try_int(s):
        try:
            return int(s)
        except ValueError:
            return s

    def alphanum_key(s):
        """Turn a string into a list of string and number chunks.

        For instance : "z23a" -> ["z", 23, "a"]
        """
        return [try_int(c) for c in re.split('([0-9]+)', s)]

    the_list.sort(key=alphanum_key)
    return the_list


def _linux_os_release():
    """This function tries to determine the name of a Linux distribution.
    It checks for the /etc/os-release file. It takes the name from the
    'NAME' field and the version from 'VERSION_ID'.
    An empty string is returned if the above values cannot be determined.
    """
    pretty_name = ''
    ashtray = {}
    keys = ['NAME', 'VERSION_ID']
    try:
        with open(os.path.join('/etc', 'os-release')) as f:
            for line in f:
                for key in keys:
                    if line.startswith(key):
                        ashtray[key] = line.strip().split('=')[1][1:-1]
    except OSError:
        return pretty_name

    if ashtray:
        if 'NAME' in ashtray:
            pretty_name = ashtray['NAME']
        if 'VERSION_ID' in ashtray:
            pretty_name += ' {0}'.format(ashtray['VERSION_ID'])

    return pretty_name


def readable_os_version():
    """Give a proper name for OS version

    :return: Proper OS version
    :rtype: str
    """
    if platform.system() == 'Linux':
        return _linux_os_release()
    elif platform.system() == 'Darwin':
        return ' {version}'.format(version=platform.mac_ver()[0])
    elif platform.system() == 'Windows':
        return platform.platform()

def check_if_file_exists(output_dir, file_name, extension):
    """The method checks if a file exists, and if it does, then it adds an increment to the filename.
    This is done until there are no longer a clash with the filename.

    :param output_dir: The directory in which the file is stored.
    :param output_dir: str

    :param file_name: The name which to use for the file.
    :type file_name: str

    :param extension: The output file extension.
    :type extension: str

    :returns: Returns the updated name for the output file which will have no clashes with existing files.
    :rtype: str
    """
    cur_file_name = file_name
    file_full_dir = '{}\\{}{}'.format(output_dir, cur_file_name, extension)

    i = 1
    while True:  # Will break out of the loop if no clash is found
        if os.path.exists(file_full_dir):  # Filename exists, add counter value
            cur_file_name = '{}_{}'.format(file_name, str(i))
            file_full_dir = '{}\\{}{}'.format(output_dir, cur_file_name, extension)
            i = i + 1
        else:  # Filename does not exist, use current filename
            break

    return cur_file_name
