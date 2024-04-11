from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.utils import hash_password
from common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            password,
            **extra_fields
    ):
        user = self.model(
            email=self.normalize_email(email),
            password=hash_password(password),
            **extra_fields
        )
        user._password = hash_password(password)
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


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    last_login = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    has_2fa = models.BooleanField(default=False)
    expected_2fa = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}({self.id}) - {self.email}"
