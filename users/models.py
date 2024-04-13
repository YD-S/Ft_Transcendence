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
        user = self.model.objects.filter(username=user_data["login"])
        if user.exists():
            return user.first()
        else:
            return self.create_user(
                email=user_data["email"],
                username=user_data["login"],
                password=hash_password(user_data["login"]),
                is_oauth=True
            )


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    last_login = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    has_2fa = models.BooleanField(default=False)
    expected_2fa = models.IntegerField(null=True, blank=True)
    expiration_2fa = models.DateTimeField(null=True, blank=True)
    is_oauth = models.BooleanField(default=False)

    verified_email = models.BooleanField(default=False)
    email_code = models.CharField(max_length=255, null=True, blank=True)
    email_code_expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}({self.id}) - {self.email}"
