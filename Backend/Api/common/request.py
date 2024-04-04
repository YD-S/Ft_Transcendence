import json

from django.core.handlers.wsgi import WSGIRequest

from users.models import User


def wrap_funcview(func):
    def wrapper(req, *args, **kwargs):
        request = req
        if not isinstance(request, HttpRequest):
            user = request.user
            request = HttpRequest(request.environ)
            request.user = user
        return func(request, *args, **kwargs)

    return wrapper


class HttpRequest(WSGIRequest):
    user: User | None = None

    # Wrap the request object to add some utility methods
    def __init__(self, environ):
        super().__init__(environ)

    def json(self):
        if self.content_type != 'application/json':
            raise ValueError('Request content type is not application/json')
        if not self.body:
            return {}
        return json.loads(self.body.decode())
