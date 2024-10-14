from common.request import HttpRequest
from users.models import User, Tournament, BlockedUser, Friendship
from users.serializers import UserSerializer, TournamentSerializer, BlockedUserSerializer, FriendshipSerializer
from utils.modelviewset import ModelViewSet


class UserViewSet(ModelViewSet):
    model = User
    serializer = UserSerializer


class TournamentViewSet(ModelViewSet):
    model = Tournament
    serializer = TournamentSerializer


class FriendshipViewSet(ModelViewSet):
    model = Friendship
    serializer = FriendshipSerializer


class BlockedUserViewSet(ModelViewSet):
    model = BlockedUser
    serializer = BlockedUserSerializer
