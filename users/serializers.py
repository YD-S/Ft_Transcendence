import datetime

from users.models import User, Tournament, BlockedUser, Friendship
from utils.modelserializer import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        excluded_fields = ['password']
        default_fields = {
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "date_joined": datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S'),
        }


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class FriendshipSerializer(ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'


class BlockedUserSerializer(ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = '__all__'
