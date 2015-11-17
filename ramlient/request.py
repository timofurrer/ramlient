# -*- coding: utf-8 -*-

"""
    Module which provides functionality to make requests
    to the API from the path of RAML nodes.
"""

import requests
from ramlfications.raml import AVAILABLE_METHODS

from .exceptions import UnsupportedHTTPMethodError, UnsupportedQueryParameter


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
            if not any(p.name == key for p in node.resource.query_params):
                raise UnsupportedQueryParameter(node.resource.path, key)

        response = requests.request(node.resource.method, node.path, params=kwargs)
        return response
    return request
