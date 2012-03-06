Apper
=====

Apper (name temporary) is a Python WSGI mini-framework designed for quick development with minimal magic.

The primary encapsulation unit is a Python module: Create functions using the provided dectorators in a module, then create an Apper instance, passing it a dictionary of the form `path_prefix -> module`.

Apper's only dependency is [WebOb](http://www.webob.org/), and can be installed with `pip install webob`.

Mini-Framework Mini-Example
=======

For more examples, check out the `examples/` dir, or for an insta-demo, run `python -m examples.simple.main` and go to [http://localhost:8080/](http://localhost:8080/).

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
