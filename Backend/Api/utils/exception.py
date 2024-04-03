class HttpError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


class NotFoundError(HttpError):
    def __init__(self):
        super().__init__(404, 'Not found')


class ValidationError(HttpError):
    def __init__(self, message: str):
        super().__init__(400, message)


class InternalServerError(HttpError):
    def __init__(self, message: str):
        super().__init__(500, message)
