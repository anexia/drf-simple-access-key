DRF Simple Auth Key
===================

A library that allows to implement a simple token authorization for Django Rest Framework.

# Installation

With a [correctly configured](https://pipenv.pypa.io/en/latest/basics/#basic-usage-of-pipenv) `pipenv` toolchain:

```sh
pipenv install git+https://github.com/anexia-it/drf-simple-access-key@main
```

You may also use classic `pip` to install the package:

```sh
pip install git+https://github.com/anexia-it/drf-simple-access-key@main
```


# Configuration

Extend django settings

```python
SIMPLE_ACCESS_KEY_SETTINGS = {
    "HTTP_AUTHORIZATION_HEADER": "x-authorization",
    "HTTP_AUTHORIZATION_SCHEME": "bearer",
    "AUTHORIZATION_KEYS": ['token'],
}
```

Extend DRF settings

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_PERMISSION_CLASSES': [
        'drf_simple_access_key.SimpleAccessKey',
    ],
    # ...
}
```

## Available settings

* **HTTP_AUTHORIZATION_HEADER**: string, name of header used for authorization
* **HTTP_AUTHORIZATION_SCHEME**: string, name of scheme used for authorization
* **AUTHORIZATION_KEYS**: string or lists of strings to be used as authorization keys

## How to use

All endpoints of the API where the permission class is used will be now protected by token authentication.

```
GET http://my.tld/api/v1/resource/
x-authorization: bearer token
```

# List of developers

* Andreas Stocker <AStocker@anexia-it.com>
* Harald Nezbeda <HNezbeda@anexia-it.com>
