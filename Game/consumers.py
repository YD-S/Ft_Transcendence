import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    players = 0
    player_names = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_id = None

    async def connect(self):
        if self.players < 2:
            await self.accept()
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
            await self.create_group(self.game_id)
            self.player_names.append(self.scope['user'].username)
            self.players += 1
        else:
            await self.close(400)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']
        direction = text_data_json['direction']
        y = text_data_json['y']
        amIfirst = text_data_json['amIfirst']
        playerId = text_data_json['playerId']

        if message == 'move':
            if direction == 'left':
                y += 0.01 if not amIfirst else -0.01
            elif direction == 'right':
                y += -0.01 if not amIfirst else 0.01

            await self.channel_layer.group_send(
                self.game_id,
                {
                    'type': 'move',
                    'data': {
                        'y': y,
                        'playerId': playerId
                    }
                }
            )

    async def create_group(self, group_name):
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )

    async def move(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'y': data['y'],
            'playerId': data['playerId']
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name
        )
        self.players -= 1
        if self.scope['user'].username in self.player_names:
            self.player_names.remove(self.scope['user'].username)
