# -*- coding: utf-8 -*-

"""
    Test ramlient.core module
"""


from unittest import TestCase
from sure import expect
import types

from ramlient.core import Client, Node, ParameterizedNode
from ramlient.errors import UnsupportedResourceMethodError, UnsupportedQueryParameter


class TestCore(TestCase):
    """
        Test core module
    """
    SIMPLE_RAML_URL = "https://raw.githubusercontent.com/spotify/ramlfications/master/tests/data/examples/simple.raml"
    GITHUB_RAML_URL = "https://raw.githubusercontent.com/spotify/ramlfications/master/tests/data/examples/github.raml"

    def test_creating_client_from_raml_url(self):
        """
            Test creating client from a RAML file per URL
        """
        client = Client(self.SIMPLE_RAML_URL)
        expect(client.raml.title).to.be.equal("Example API")

    def test_accessing_first_level_resource(self):
        """
            Test accessing first level resource
        """
        client = Client(self.SIMPLE_RAML_URL)
        resource = client.resource
        expect(resource).to.be.a(Node)
        expect(resource.path).to.be.equal("/resource")
        expect(resource.resource.display_name).to.be.equal("First One")

    def test_accessing_second_level_resource(self):
        """
            Test accessing second level resource
        """
        client = Client(self.GITHUB_RAML_URL)
        resource = client.search.repositories
        expect(resource).to.be.a(Node)
        expect(resource.path).to.be.equal("/search/repositories")

    def test_accessing_dynamic_resource(self):
        """
            Test accessing dynamic resource
        """
        client = Client(self.SIMPLE_RAML_URL)
        resource = client.resource.resourceId(5)
        expect(resource).to.be.a(ParameterizedNode)
        expect(resource.resource.path).to.be.equal("/resource/{resourceId}")
        expect(resource.parameter).to.be.equal({"resourceId": 5})
        expect(resource.path).to.be.equal("/resource/5")

    def test_getting_request_method_from_resource(self):
        """
            Test getting request method from resource
        """
        client = Client(self.SIMPLE_RAML_URL)
        expect(client.resource.get).to.be.a(types.FunctionType)
        expect(client.resource.put).to.be.a(types.FunctionType)
        expect(client.resource.delete).to.be.a(types.FunctionType)
        expect(client.resource.patch).to.be.a(types.FunctionType)
        expect(client.resource.options).to.be.a(types.FunctionType)
        expect(client.resource.trace).to.be.a(types.FunctionType)
        expect(client.resource.connect).to.be.a(types.FunctionType)
        try:
            client.resource.post
        except UnsupportedResourceMethodError as e:
            expect(str(e)).to.be.equal("Resource '/resource' does not support method 'post'")
        else:
            RuntimeError("Should not enter here")

        expect(client.resource.resourceId(5).get).to.be.a(types.FunctionType)
        expect(client.resource.resourceId(5).post).to.be.a(types.FunctionType)

        try:
            client.resource.resourceId(5).delete
        except UnsupportedResourceMethodError as e:
            expect(str(e)).to.be.equal("Resource '/resource/{resourceId}' does not support method 'delete'")
        else:
            RuntimeError("Should not enter here")

    def test_passing_query_parameter_to_resource(self):
        """
            Test passing query parameter to resource
        """
        client = Client(self.SIMPLE_RAML_URL)
        try:
            client.resource.resourceId(5).get(foo="42")
        except UnsupportedQueryParameter as e:
            expect(str(e)).to.be.equal("Resource '/resource/{resourceId}' does not support Query Parameter 'foo'")
        else:
            RuntimeError("Should not enter here")

        # client.resource.resourceId(5).get(filter="42")

    def test_passing_wrong_typed_query_parameter_to_resource(self):
        """
            Test passing wrong typed query parameter to resource
        """
        client = Client(self.SIMPLE_RAML_URL)
        try:
            client.resource.resourceId(5).get(filter=42)
        except TypeError as e:
            expect(str(e)).to.be.equal("Resource Query Parameter has type 'int' but expected type 'string'")
        else:
            RuntimeError("Should not enter here")
