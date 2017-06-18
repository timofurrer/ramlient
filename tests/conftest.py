# -*- coding: utf-8 -*-

"""
    ramlient
    ~~~~~~~~

    Access to a RAML API done right, in Python.

    :copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

import os

import pytest

from ramlient import Client


__DATA_DIR__ = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/'))
__EXAMPLES_DIR__ = os.path.join(__DATA_DIR__, 'examples')
__EXAMPLES_CONFIG_TPL__ = os.path.join(__DATA_DIR__, 'examples', '{name}-config.ini')


@pytest.fixture(scope='function')
def example_client(request):
    """
    Fixture which creates a new client based
    on an example API from tests/data/examples.
    """
    example_name = request.param
    example_path = os.path.join(__EXAMPLES_DIR__, example_name + '.raml')
    example_config = __EXAMPLES_CONFIG_TPL__.format(name=example_name)
    if not os.path.exists(example_config):
        example_config = None

    client = Client(example_path, ramlconfig=example_config)
    return client
