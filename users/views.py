
from common.request import HttpRequest
from users.models import User
from users.serializers import UserSerializer
from utils.modelviewset import ModelViewSet


class UserViewSet(ModelViewSet):
    model = User
    serializer = UserSerializer

    def list(self, request: HttpRequest, *args, **kwargs):
        print(request.user)
        return super().list(request, *args, **kwargs)
