import django
django.setup()

import json
from channels.generic.websocket import WebsocketConsumer

from chat.models import Room


class ChatRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room: Room = None

    def connect(self):
        # Check the path to the room
        try:
            room_id = int(self.scope['url_route']['kwargs']['room_id'])
        except ValueError:
            self.close()
            return
        # try:
        #     self.room = Room.objects.get(id=room_id)
        # except Room.DoesNotExist:
        #     self.close()
        #     return
        self.accept()

        # send the last 10 messages
        # messages = self.room.messages.order_by('-created_at')[:10]
        # for message in reversed(messages):
        #     self.send(text_data=json.dumps({
        #         'message': message.content
        #     }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data: str):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Message.objects.create(content=message, sender=self.scope['user'], room=self.room).save()
        self.send(text_data=json.dumps({
            'message': message + " from server"
        }))
