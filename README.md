Apper
=====

Apper (name temporary) is a Python WSGI mini-framework designed for quick development with minimal magic.

The primary encapsulation unit is a Python module: Create functions using the provided dectorators in a module, then create an Apper instance, passing it a dictionary of the form `path_prefix -> module`.

Example
=======

hello.py
--------

```python
from apper import get

@get("<name>")
def hello(req, resp, name):
    return "Hello, %s!" % name

@get
def hello_world(req, resp):
    return hello_name(req, resp, "world")
```

app.py
------

```python
from apper import Apper

import hello

app = Apper({
    '/hello': hello
})
```

Serve `app` with your favorite WSGI server, then go to `/hello/insert_name_here` for a pleasant greeting.
