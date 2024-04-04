from django.db import models

from authentication.utils import hash_password
from common.models import BaseModel


class User(BaseModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        print(self.password)
        self.password = hash_password(self.password)
        print(self.password)
        super().save(*args, **kwargs)
