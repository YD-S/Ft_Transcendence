from django.contrib.auth.backends import BaseBackend

from authentication.utils import hash_password
from users.models import User


class TokenBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        password_hash = hash_password(password)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if user.password != password_hash:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
