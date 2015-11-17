# ramlient - client for RAML backends in python
> RESTful API Modeling Language (RAML) client

***

Author: Timo Furrer <tuxtimo@gmail.com> <br>
License: **MIT** <br>

***

## What?

The name `ramlient` is combined from `RAML` and `client`. As the name says, `ramlient` automatically creates a python client for APIs providing a RAML file.

## Installation

Use pip to install `ramlient`:

```bash
pip install ramlient
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
