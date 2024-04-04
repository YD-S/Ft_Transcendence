from authentication.utils import require_token
from users.models import User
from users.serializers import UserSerializer
from utils.modelviewset import ModelViewSet


class UserViewSet(ModelViewSet):
    def __init__(self):
        super().__init__(User, UserSerializer)
        self.decorators = [
            require_token
        ]
