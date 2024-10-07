from common.request import HttpRequest
from users.models import User, Tournament
from users.serializers import UserSerializer, TournamentSerializer
from utils.modelviewset import ModelViewSet


class UserViewSet(ModelViewSet):
    model = User
    serializer = UserSerializer


class TournamentViewSet(ModelViewSet):
    model = Tournament
    serializer = TournamentSerializer
