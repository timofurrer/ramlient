# -*- coding: utf-8 -*-

"""
    Test ramlient.core module
"""

import types

import pytest

from ramlient.core import Node, ParameterizedNode
from ramlient.errors import UnsupportedResourceMethodError, UnsupportedQueryParameter


@pytest.mark.parametrize('example_client', [
    'simple'
], indirect=['example_client'])
def test_creating_client_from_raml_url(example_client):
    """
        Test creating client from a RAML file per URL
    """
    assert example_client.raml.title == 'Example API'


@pytest.mark.parametrize('example_client', [
    'simple'
], indirect=['example_client'])
def test_accessing_first_level_resource(example_client):
    """
        Test accessing first level resource
    """
    # given & when
    resource = example_client.resource

    # then
    assert isinstance(resource, Node)
    assert resource.path == '/resource'
    assert resource.resource.display_name == 'First One'


@pytest.mark.parametrize('example_client', [
    'github'
], indirect=['example_client'])
def test_accessing_second_level_resource(example_client):
    """
        Test accessing second level resource
    """
    # given & when
    resource = example_client.search.repositories

    # then
    assert isinstance(resource, Node)
    assert resource.path == '/search/repositories'


@pytest.mark.parametrize('example_client', [
    'simple'
], indirect=['example_client'])
def test_accessing_dynamic_resource(example_client):
    """
        Test accessing dynamic resource
    """
    # given & when
    resource = example_client.resource.resourceId(5)

    # then
    assert isinstance(resource, ParameterizedNode)
    assert resource.resource.path == '/resource/{resourceId}'
    assert resource.parameter == {"resourceId": 5}
    assert resource.path == '/resource/5'


@pytest.mark.parametrize('example_client', [
    'simple'
], indirect=['example_client'])
def test_getting_request_method_from_resource(example_client):
    """
        Test getting request method from resource
    """
    assert isinstance(example_client.resource.get, types.FunctionType)
    assert isinstance(example_client.resource.put, types.FunctionType)
    assert isinstance(example_client.resource.delete, types.FunctionType)
    assert isinstance(example_client.resource.patch, types.FunctionType)
    assert isinstance(example_client.resource.options, types.FunctionType)
    assert isinstance(example_client.resource.trace, types.FunctionType)
    assert isinstance(example_client.resource.connect, types.FunctionType)

    # when
    with pytest.raises(UnsupportedResourceMethodError) as exc:
        example_client.resource.post  # noqa

    # then
    assert str(exc.value) == "Resource '/resource' does not support method 'post'"

    # then
    assert isinstance(example_client.resource.resourceId(5).get, types.FunctionType)
    assert isinstance(example_client.resource.resourceId(5).post, types.FunctionType)

    # when
    with pytest.raises(UnsupportedResourceMethodError) as exc:
        example_client.resource.resourceId(5).delete  # noqa

    # then
    assert str(exc.value) == "Resource '/resource/{resourceId}' does not support method 'delete'"


@pytest.mark.parametrize('example_client', [
    'simple'
], indirect=['example_client'])
def test_passing_query_parameter_to_resource(example_client):
    """
        Test passing query parameter to resource
    """
    # when
    with pytest.raises(UnsupportedQueryParameter) as exc:
        example_client.resource.resourceId(5).get(foo=42)

    # then
    assert str(exc.value) == "Resource '/resource/{resourceId}' does " \
        "not support Query Parameter 'foo'"


@pytest.mark.parametrize('example_client', [
    'simple'
], indirect=['example_client'])
def test_passing_wrong_typed_query_parameter_to_resource(example_client):
    """
        Test passing wrong typed query parameter to resource
    """
    # when
    with pytest.raises(TypeError) as exc:
        example_client.resource.resourceId(5).get(filter=42)

    # then
    assert str(exc.value) == "Resource Query Parameter has type 'int' but expected type 'string'"
