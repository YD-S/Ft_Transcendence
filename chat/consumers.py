import django

django.setup()

import datetime
from asgiref.sync import async_to_sync

from chat.serializers import MessageSerializer

import json
from channels.generic.websocket import WebsocketConsumer

from chat.models import Room, Message


class ChatRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group = None

    def send_group(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.group,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    def connect(self):
        self.group = f"chat_{self.scope['url_route']['kwargs']['room_id']}"
        async_to_sync(self.channel_layer.group_add)(
            self.group, self.channel_name
        )
        self.accept()
        self.send_group({
            'user_id': self.scope['user'].id,
            'content': f'<a href="/user?id={self.scope["user"].id}">{self.scope["user"].username}</a> has joined the chat',
            'created_at': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
        })

    def disconnect(self, close_code):
        self.send_group({
            'user_id': self.scope['user'].id,
            'content': f'<a href="/user?id={self.scope["user"].id}">{self.scope["user"].username}</a> has left the chat',
            'created_at': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
        })
        async_to_sync(self.channel_layer.group_discard(self.group, self.channel_name))

    def receive(self, text_data):
        room = Room.objects.get(id=int(self.scope['url_route']['kwargs']['room_id']))

        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        msg = Message.objects.create(content=message, sender=self.scope['user'], room=room)
        msg.save()
        self.send_group(MessageSerializer(instance=msg).data)

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
