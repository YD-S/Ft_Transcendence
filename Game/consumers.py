import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    players = 0
    player_names = []

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_id = None

    def connect(self):
        if self.players < 2:
            self.accept()
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
            self.create_group(self.game_id + self.scope['user'].username)
            self.player_names.append(self.scope['user'].username)
            print(self.game_id)
        else:
            return
        self.players += 1

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']
        direction = text_data_json['direction']
        y = text_data_json['y']
        player_id = text_data_json['playerId']
        if message == 'move':
            if direction == 'left':
                if player_id:
                    y = y + 0.1
                else:
                    y = y - 0.1
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id + self.player_names[0],
                    {
                        'type': 'move',
                        'data': {
                            'y': y,
                        }
                    }
                )
            elif direction == 'right':
                if player_id:
                    y = y - 0.1
                else:
                    y = y + 0.1
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id + self.player_names[1],
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
        print('event', event)
        data = event['data']
        self.send(text_data=json.dumps({
            'type': event['type'],
            'y': data['y'],
        }))
