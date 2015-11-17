# -*- coding: utf-8 -*-

"""
    Utility functions used in ramlient.
"""

try:  # python 2.x
    from urlparse import urlparse
except ImportError:  # python 3.x
    from urllib.parse import urlparse

import requests

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
