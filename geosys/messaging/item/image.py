"""
**Paragraph.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.
"""


__author__ = 'marco@opengis.ch'
__revision__ = '$Format:%H$'
__date__ = '28/05/2013'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')

from .text import Text

# FIXME (MB) remove when all to_* methods are implemented
# pylint: disable=W0223


class Image(Text):
    """A class to model emphasized text in the messaging system."""

    def __init__(self, uri, text=None, width=None, height=None, url=None, **kwargs):
        """Creates a Emphasized Text Text object

        :param uri: A string to add to the message.
        :type uri: str

        We pass the kwargs on to the base class so an exception is raised
        if invalid keywords were passed. See:

        http://stackoverflow.com/questions/13124961/
        how-to-pass-arguments-efficiently-kwargs-in-python
        """
        super(Image, self).__init__(**kwargs)
        self.uri = uri
        if text is None:
            self.text = ''
        else:
            self.text = text

        self.url = url
        self.width = width
        self.height = height

    def to_html(self):
        """Render as html.
        """
        html_attributes = ''
        if self.width is not None:
            html_attributes = "width=%s" % (str(self.width))
        if self.height is not None:
            html_attributes = "%s height=%s" % (html_attributes, str(self.height))

        final_html = '<img src="%s" title="%s" alt="%s" %s/>' % (self.uri, self.text, self.text, str(html_attributes))

        if self.url is not None:
            final_html = '<p><a href="%s">%s</a></p>' % (self.url, final_html)

        return final_html

    def to_text(self):
        """Render as plain text.
        """
        if self.text == '':
            return '::%s' % self.uri
        return '::%s [%s]' % (self.text, self.uri)
