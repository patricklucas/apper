import inspect
import re

import webob
import webob.exc


class Action(object):

    def __init__(self, method, path, fn):
        super(Action, self).__init__()
        self.method = method
        self._compile_path(path)
        self.fn = fn

    def _compile_path(self, path):
        self.uri_template = re.sub(r"<([a-zA-Z0-9_]+)>", r"%(\1)s", path)

        route_re = path.replace('.', '\.')
        route_re = re.sub(r"<([a-zA-Z0-9_]+)>", r"(?P<\1>[^./]+)", route_re)
        route_re = '^' + route_re + '/?$'
        self.route = re.compile(route_re)

    def uri(self, **kwargs):
        return '/' + self.servlet + '/' + self.uri_template % kwargs

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def action_dec(method=None):
    def path_dec(path=None):
        # Let decorator be called like '@get' or '@get("my/path")'
        if callable(path):
            fn = path
            path = ""
            return Action(method, path, fn)
        else:
            if path is None:
                path = ""
    
            def dec(fn):
                return Action(method, path, fn)
            return dec
    return path_dec

get = action_dec('GET')
post = action_dec('POST')
put = action_dec('PUT')
delete = action_dec('DELETE')


class Apper(object):

    def __init__(self, servlets):
        super(Apper, self).__init__()
        self.routes = {}

        def isaction(member):
            return isinstance(member, Action)

        # Create a dict like:
        #
        # foo:
        #   GET: [action, action]
        #   POST: [action]
        # bar:
        #   GET: [action]
        for name, module in servlets.iteritems():
            matches = re.match(r"/?([a-zA-Z0-9_-]*)$", name)
            if not matches:
                raise ValueError("Invalid servlet name '%s'" % name)
            name = matches.group(1) # 'name' without leading /

            if name in self.routes:
                raise ValueError("Duplicate servlet name '%s'" % name)

            routes = self.routes[name] = {}
            for _, action in inspect.getmembers(module, predicate=isaction):
                action.servlet = name
                routes.setdefault(action.method, []).append((action.route, action.fn))

    def route(self, request):
        servlet_name = request.path_info_pop()

        if servlet_name not in self.routes:
            raise webob.exc.HTTPNotFound

        for route, action in self.routes[servlet_name].get(request.method, []):
            matches = route.match(request.path_info[1:]) # Strip leading /
            if matches:
                return action, matches.groupdict()

        raise webob.exc.HTTPNotFound

    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        response = webob.Response(request=request)

        try:
            action, params = self.route(request)
            content = action(request, response, **params)

            # Allow use of generator functions
            if isinstance(content, basestring):
                response.body = content
            else:
                response.app_iter = content
        except webob.exc.WSGIHTTPException as e:
            return request.get_response(e)(environ, start_response)
        else:
            return response(environ, start_response)
