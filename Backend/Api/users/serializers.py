from users.models import User
from utils.modelserializer import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        excluded_fields = ['password']
