import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    players = 0

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_id = None

    def connect(self):
        if self.players < 2:
            self.accept()
        else:
            pass
        if self.players == 2:
            self.create_group(self.scope["url_route"]["kwargs"]["game_id"])
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.players += 1

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']
        direction = text_data_json['direction']
        y = text_data_json['y']
        playerId = text_data_json['playerId']
        if message == 'move':
            if direction == 'left':
                if playerId:
                    y = y + 0.1
                else:
                    y = y - 0.1
                async_to_sync(self.channel_layer.group_send)(
                    self.scope['user'].username,
                    {
                        'type': 'move',
                        'data': {
                            'y': y,
                        }
                    }
                )
            elif direction == 'right':
                if playerId:
                    y = y - 0.1
                else:
                    y = y + 0.1
                async_to_sync(self.channel_layer.group_send)(
                    self.scope['user'].username,
                    {
                        'type': 'move',
                        'data': {
                            'y': y,
                        }
                    }
                )
    def create_group(self, group_name):
        async_to_sync(self.channel_layer.group_add)(
            group_name,
            self.channel_name
        )

    def move(self, event):
        data = event['data']
        self.send(text_data=json.dumps({
            'type': event['type'],
            'y': data['y'],
        }))

