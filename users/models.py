import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.utils import hash_password
from common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            password=hash_password(password),
            **extra_fields
        )
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            password=hash_password(password),
            **extra_fields
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user

    def get_or_create_42_user(self, data):
        access_token = data.get("access_token")
        response = requests.get('https://api.intra.42.fr/v2/me', headers={"Authorization": f"Bearer {access_token}"})
        user_data = response.json()
        user = self.model.objects.filter(username=user_data["login"] + "@42")
        if user.exists():
            return user.first()
        else:
            return self.create_user(
                email=user_data["email"],
                username=user_data["login"] + "@42",
                password=hash_password(user_data["login"]),
                is_oauth=False,
                verified_email=True
            )


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    last_login = models.DateTimeField(null=True, blank=True)

    has_2fa = models.BooleanField(default=False)
    is_oauth = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to="avatars/", null=True, default='svg/profile_icon.svg')

    objects = UserManager()

    def __str__(self):
        return f"{self.username}({self.id}) - {self.email}"


class Match(BaseModel):
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_matches")
    loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lost_matches")
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.winner} vs {self.loser} | {self.winner_score} - {self.loser_score}"


class Friendship(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_of")

    def __str__(self):
        return f"{self.user} - {self.friend}"

