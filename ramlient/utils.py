# -*- coding: utf-8 -*-

"""
    ramlient
    ~~~~~~~~

    Access to a RAML API done right, in Python.

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import sys

try:  # python 2.x
    from urlparse import urlparse
except ImportError:  # python 3.x
    from urllib.parse import urlparse

import requests

if sys.version_info[0] == 2:  # python 2.x
    TYPES_MAPPING = {
        "string": (str, unicode),  # noqa
        "integer": int
    }
else:  # python 3.x
    TYPES_MAPPING = {
        "string": str,
        "integer": int
    }


def download_file(url):
    """
        Downloads a file from the specified URL.

        :param str url: The URL to the file to be downloaded

        :returns: the downloaded file's content
        :rtype: str
    """
    response = requests.get(url)
    if response.status_code is not 200:
        return None
    return response.text


def is_url(url):
    """
        Check if given URL is a valid URL.

        :param str url: The url to validate

        :returns: if the url is valid or not
        :rtype: bool
    """
    return urlparse(url).scheme != ""


def match_type(value, expected_type):
    """
        Checks if the given value type matches the
        expected type

        :param value: the value which's type should be checked
        :param str expected_type: the name of the expected value

        :returns: if the value has the expected type or not
        :rtype: bool
    """
    try:
        return isinstance(value, TYPES_MAPPING[expected_type])
    except KeyError:
        return False
