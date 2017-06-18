# -*- coding: utf-8 -*-

"""
    Test ramlient.utils module.
"""

import pytest

from ramlient import utils


@pytest.mark.parametrize('url, is_url', [
    ('http://foo.com', True),
    ('http://foo.com/bar', True),
    ('http://foo.com/bar#foo', True),
    ('http://foo.com/bar.txt?foo=bar', True),
    ('bar.txt', False),
    ('/usr/bin/', False),
    ('../bar.txt', False),
    ('./bar.txt', False)
])
def test_is_url_function(url, is_url):
    """
        Test if "is_url" function works
    """
    # then
    assert utils.is_url(url) is is_url


@pytest.mark.parametrize('value, expected_type, does_match', [
    ('Hello', 'string', True),
    ('Hello', 'integer', False),
    (42, 'integer', True),
    (42, 'string', False),
    (42, 'weird_type', False),
])
def test_match_type_function(value, expected_type, does_match):
    """
        Test if "match_type" function works
    """
    # then
    assert utils.match_type(value, expected_type) is does_match
