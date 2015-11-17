# -*- coding: utf-8 -*-

"""
    Module which provides functionality to make requests
    to the API from the path of RAML nodes.
"""

import requests

from .exceptions import UnsupportedHTTPMethodError


SUPPORTED_METHODS = ["OPTIONS", "CONNECT", "TRACE", "PATCH", "DELETE", "GET", "POST", "PUT"]


def prepare_request(node):
    """
        Prepare request to node's API route

        :param Node node: the RAML node object
    """
    if node.resource.method.upper() not in SUPPORTED_METHODS:
        raise UnsupportedHTTPMethodError(node.resource.method)


    def request(**kwargs):
        """
            Make request to node's API route with the given keyword arguments
        """
        # TODO: check if kwargs are valid
        response = requests.request(node.resource.method, node.path)
        return response
    return request
