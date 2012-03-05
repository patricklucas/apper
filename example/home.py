from apper import get

@get
def home(req, resp):
    return """
<h1>Welcome!</h1>
<form action="/hello" method="post">
Name: <input type="text" name="name" />
<input type="submit" value="Go!" />
</form>
"""
