from wsgiref.simple_server import make_server

from apper import Apper

import home
import hello

app = Apper({
    '/': home,
    '/hello': hello
})

if __name__ == '__main__':
    make_server('0.0.0.0', 8080, app).serve_forever()
