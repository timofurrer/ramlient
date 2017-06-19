# -*- coding: utf-8 -*-

"""
    ramlient
    ~~~~~~~~

    Access to a RAML API done right, in Python.

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import requests
from ramlfications.raml import AVAILABLE_METHODS

from .utils import match_type
from .errors import UnsupportedHTTPMethodError, UnsupportedQueryParameter


def prepare_request(node):
    """
        Prepare request to node's API route

        :param Node node: the RAML node object
    """
    if node.resource.method not in AVAILABLE_METHODS:
        raise UnsupportedHTTPMethodError(node.resource.method)

    def request(**kwargs):
        """
            Make request to node's API route with the given keyword arguments
        """
        # validate given query parameters
        for key, value in kwargs.items():
            param = next((p for p in node.resource.query_params if p.name == key), None)
            if not param:
                raise UnsupportedQueryParameter(node.resource.path, key)

            if not match_type(value, param.type):
                raise TypeError(
                    "Resource Query Parameter has type '{0}' but expected type '{1}'".format(
                        value.__class__.__name__, param.type))

        response = requests.request(node.resource.method, node.resource.absolute_uri, params=kwargs)
        return response
    return request
