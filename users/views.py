from common.request import HttpRequest
from users.models import User, Tournament, BlockedUser
from users.serializers import UserSerializer, TournamentSerializer, BlockedUserSerializer
from utils.modelviewset import ModelViewSet


class UserViewSet(ModelViewSet):
    model = User
    serializer = UserSerializer


class TournamentViewSet(ModelViewSet):
    model = Tournament
    serializer = TournamentSerializer


class BlockedUserViewSet(ModelViewSet):
    model = BlockedUser
    serializer = BlockedUserSerializer
