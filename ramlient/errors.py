# -*- coding: utf-8 -*-

"""
    ramlient
    ~~~~~~~~

    Access to a RAML API done right, in Python.

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""


class RamlientError(Exception):
    """
        Base Exception for all ramlient based Exceptions
    """
    pass


class ResourceNotFoundError(RamlientError):
    """
        Exception which is raised if a certain resource does not exist
    """
    def __init__(self, resource_path):
        super(ResourceNotFoundError, self).__init__(
            'No such Resource found: {0}'.format(resource_path))


class UnsupportedHTTPMethodError(RamlientError):
    """
        Exception which is raised if a certain HTTP method is not supported
    """
    def __init__(self, method):
        super(UnsupportedHTTPMethodError, self).__init__('No such HTTP method: {0}'.format(method))


class UnsupportedResourceMethodError(RamlientError):
    """
        Exception which is raised if the certain resource does not support the certain method
    """
    def __init__(self, resource_path, method):
        super(UnsupportedResourceMethodError, self).__init__(
            "Resource '{0}' does not support method '{1}'".format(resource_path, method))


class UnsupportedQueryParameter(RamlientError):
    """
        Exception which is raised if the certain resource does not
        support the certain query parameter
    """
    def __init__(self, resource_path, query_parameter):
        super(UnsupportedQueryParameter, self).__init__(
            "Resource '{0}' does not support Query Parameter '{1}'".format(
                resource_path, query_parameter))
