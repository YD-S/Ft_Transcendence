from django.db import models

from common.models import BaseModel
from users.models import User


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
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField('users.User', related_name='rooms')
    is_direct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.members.all()}"

    class Meta:
        ordering = ['created_at']

    def get_direct_name(self, user: User) -> str:
        if self.is_direct:
            return self.members.exclude(id=user.id).first().username
        return "None"

    def join(self, user: User):
        self.members.add(user)

    def leave(self, user: User):
        self.members.remove(user)
        if self.members.count() == 0:
            self.delete()
