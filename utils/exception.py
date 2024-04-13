from django.http import HttpResponse


class HttpError(Exception):
    def __init__(self, status: int, content: str):
        self.status = status
        self.content = content
        self.content_type = 'text/plain'

    def as_http_response(self):
        return HttpResponse(content=self.content, content_type=self.content_type, status=self.status)


class UnauthorizedError(HttpError):
    def __init__(self):
        super().__init__(401, '{"message": "Unauthorized", "type": "unauthorized"}')
        self.content_type = 'application/json'


class NotFoundError(HttpError):
    def __init__(self):
        super().__init__(404, 'Not found')


class ValidationError(HttpError):
    def __init__(self, content: str, content_type: str = 'text/plain'):
        super().__init__(400, content)
        self.content_type = content_type


class InternalServerError(HttpError):
    def __init__(self, content: str):
        super().__init__(500, content)
