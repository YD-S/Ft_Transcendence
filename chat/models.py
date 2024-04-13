import random

from django.db import models

from common.models import BaseModel
from users.models import User
from utils.exception import ValidationError


# Create your models here.
class Message(BaseModel):
    content = models.TextField()
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    room = models.ForeignKey('chat.Room', on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        if self.room.is_direct:
            return f"{self.sender.username}: {self.content}"
        return f"{self.sender.username} on {self.room}: {self.content}"

    class Meta:
        ordering = ['created_at']


class Room(BaseModel):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField('users.User', related_name='rooms')
    is_direct = models.BooleanField(default=False)
    code = models.CharField(max_length=8, unique=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.members.all()}"

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def get_name(self, user: User) -> str:
        if self.is_direct:
            return self.members.exclude(id=user.id).first().username
        return self.name

    def join(self, user: User):
        if self.is_direct and self.members.count() == 2:
            raise ValidationError("Direct rooms can only have 2 members")
        self.members.add(user)

    def leave(self, user: User):
        self.members.remove(user)
        if self.members.count() == 0:
            self.delete()

    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
