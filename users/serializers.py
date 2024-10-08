import datetime

from users.models import User, Tournament
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
