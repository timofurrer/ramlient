# -*- coding: utf-8 -*-

"""
    ramlient
    ~~~~~~~~

    Access to a RAML API done right, in Python.

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import codecs
from collections import namedtuple

try:  # python 2.x
    from urlparse import urljoin
except ImportError:  # python 3.x
    from urllib.parse import urljoin

import ramlfications

from . import utils
from .request import AVAILABLE_METHODS, prepare_request
from .errors import ResourceNotFoundError, UnsupportedResourceMethodError

NodeParameter = namedtuple("NodeParameter", ["resource", "parameter"])


class Node(object):
    """
        Wrapper for the RAML ResourceNode
    """
    def __init__(self, client, resource):
        self.client = client
        self.resource = resource

    def __repr__(self):
        return "<Node ({0})>".format(repr(self.resource))

    def __getattr__(self, attr):
        """
            Accessing sub node
        """
        if attr in AVAILABLE_METHODS:
            self._patch_resource(attr)
            return prepare_request(self)

        resource = self.client.get_resource(self.resource.path + "/", attr)
        if not resource:
            raise ResourceNotFoundError(self.resource.path + "/" + attr)

        if hasattr(resource, "parameter"):
            return lambda x: ParameterizedNode(
                self.client, resource.resource, {resource.parameter: x})
        else:
            return Node(self.client, resource)

    @property
    def absolute_uri(self):
        """
            Returns the absolute uri for given resource, after joining the base
            uri.
        """
        return urljoin(self.client.base_uri, self.path)

    @property
    def path(self):
        """
            Returns the RAML resource node's path
        """
        return self.resource.path

    def _patch_resource(self, method):
        """
            Patch the current RAML ResourceNode by the resource with the
            correct method if it exists

            If the resource with the specified method does not exist
            an exception is raised.

            :param str method: the method of the resource

            :raises UnsupportedResourceMethodError: if resource does not support the method
        """
        resource = self.client.get_resource("", self.resource.path, method)
        if not resource:
            raise UnsupportedResourceMethodError(self.resource.path, method)

        self.resource = resource


class ParameterizedNode(Node):
    """
        Wrapper for the RAML ResourceNode combined with the values
        of the dynamic part from the URL
    """
    def __init__(self, client, resource, parameter):
        super(ParameterizedNode, self).__init__(client, resource)
        self.parameter = parameter

    def __repr__(self):
        return "<ParameterizedNode ({0}), Parameter: {1}>".format(self.resource, self.parameter)

    @property
    def path(self):
        """
            Returns the RAML resource node's path
        """
        return self.resource.path.format(**self.parameter)


class Client(object):
    """
        RAML client
    """
    def __init__(self, ramlfile, ramlconfig=None):
        self.ramlfile = ramlfile
        self.ramlconfig = ramlconfig
        self.raml = None

        self.parse_raml()
        self.base_uri = self.raml.base_uri

    def parse_raml(self):
        """
            Parse RAML file
        """
        if utils.is_url(self.ramlfile):
            raml = utils.download_file(self.ramlfile)
        else:
            with codecs.open(self.ramlfile, "rb", encoding="utf-8") as raml_f:
                raml = raml_f.read()

        loader = ramlfications.loads(raml)
        config = ramlfications.setup_config(self.ramlconfig)
        self.raml = ramlfications.parse_raml(loader, config)

    def __getattr__(self, attr):
        """
            Access ResourceNode from RAML
        """
        resource = self.get_resource("/", attr)
        if not resource:
            raise ResourceNotFoundError(attr)

        return Node(self, resource)

    def get_resource(self, base_resource_path, resource_path, method=None):
        """
            Gets a resource by it's path and optional by it's method

            This method does not care about the supported resource methods
            unless it is specified.

            :param str resource_path: The path of the resource
            :param str method: The method of the path.

            :returns: the resource if it exists or None
            :rtype: ResourceNode
        """
        basic_path = base_resource_path + resource_path
        dynamic_path = base_resource_path + "{" + resource_path + "}"
        for resource in self.raml.resources:
            method_matched = method is None or resource.method == method
            if resource.path == basic_path and method_matched:
                return resource

            if resource.path == dynamic_path and method_matched:
                return NodeParameter(resource=resource, parameter=resource_path)
        return None
