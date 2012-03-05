import webob.exc

from apper import get, post

@get("<name>")
def hello(req, resp, name):
    return "Hello, %s!" % name

@post
def hello_post(req, resp):
    if not req.POST.get('name'):
        raise webob.exc.HTTPNotFound
    
    name = req.POST['name']
    raise webob.exc.HTTPSeeOther(location=hello.uri(name=name))
