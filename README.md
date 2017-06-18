# ramlient - RAML client for python
> Access to a RAML API done right, in Python.

***

[![Build Status](https://travis-ci.org/timofurrer/ramlient.svg?branch=master)](https://travis-ci.org/timofurrer/ramlient)
[![codecov](https://codecov.io/gh/timofurrer/ramlient/branch/master/graph/badge.svg)](https://codecov.io/gh/timofurrer/ramlient)
[![Code Health](https://landscape.io/github/timofurrer/ramlient/master/landscape.svg?style=flat)](https://landscape.io/github/timofurrer/ramlient/master)
<br>
[![PyPI version](https://badge.fury.io/py/ramlient.svg)](https://badge.fury.io/py/ramlient)
[![PyPI](https://img.shields.io/pypi/pyversions/ramlient.svg)](https://pypi.python.org/pypi/ramlient)
[![PyPI](https://img.shields.io/pypi/wheel/ramlient.svg)](https://pypi.python.org/pypi/ramlient)

***

**ramlient** makes it very easy to access RAML based APIs.

## Installation

Use pip to install `ramlient`:

```bash
pip3 install ramlient
```

## Usage

Let's assume you have the following simple RAML file:

```raml
#%RAML 0.8
---
title: Example API
baseUri: http://example.com
securitySchemes:
  - basic:
      type: Basic Authentication
/resource:
  displayName: First One
  put:
    responses:
      200:
      201:
      203:
  get:
    description: get the first one
    headers:
      x-custom:
    responses:
      200:
  /{resourceId}:
    description: This is a resource description *with* some _markdown_ embedded in it
    uriParameters:
      resourceId:
        required: true
        description: Which resoure would you like to view
    get:
      queryParameters:
        filter:
          description: What to filter
          type: string
      responses:
        200:
```

Use `ramlient` to make easy requests to the routes:

```python
from ramlient import Client

client = Client("api.raml")
response = client.resource.get()
resource = client.resource.resourceId(1).get()
```
