# -*- coding: utf-8 -*-

"""
    The name `ramlient` is combined from `RAML` and `client`.
    As the name says, `ramlient` automatically creates a python
    client for APIs providing a RAML file.
"""

__VERSION__ = "0.0.1"
__LICENSE__ = "MIT"
__AUTHOR__ = "Timo Furrer"
__AUTHOR_EMAIL__ = "tuxtimo@gmail.com"
__DESCRIPTION__ = "foo"
__URL__ = ""
__DOWNLOAD_URL__ = ""

from .core import Client, Node, ParameterizedNode
