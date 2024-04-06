from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.utils import hash_password
from common.models import BaseModel


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}({self.id}) - {self.email}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = hash_password(self.password)
        return super().save(*args, **kwargs)



