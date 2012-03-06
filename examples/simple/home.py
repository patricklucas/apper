from apper import get

import hello

@get
def home(req, resp):
    hello_uri = hello.hello_post.uri()

    return """
<h1>Welcome!</h1>
<form action="%(hello_uri)s" method="post">
Name: <input type="text" name="name" />
<input type="submit" value="Go!" />
</form>
""" % locals()
