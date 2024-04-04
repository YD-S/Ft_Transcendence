from django.core.handlers.wsgi import WSGIRequest

from authentication.token import require_token
from common.request import HttpRequest
from users.models import User
from users.serializers import UserSerializer
from utils.modelviewset import ModelViewSet


class UserViewSet(ModelViewSet):
    def __init__(self):
        super().__init__(User, UserSerializer)
        self.decorators += [
            require_token
        ]

    def list(self, request: HttpRequest):
        print(request.user)
        return super().list(request)
