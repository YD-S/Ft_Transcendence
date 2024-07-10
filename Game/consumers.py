import asyncio
import json
import math
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    players = 0
    player_names = []
    player1_y = math.pi / 2
    player2_y = -math.pi / 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player1 = None
        self.player2 = None
        self.game_id = None
        self.frame_task = None  # Task to manage the frame sending coroutine

    async def connect(self):
        if GameConsumer.players < 2:
            await self.accept()
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
            await self.create_group(self.game_id)
            self.player_names.append(self.scope['user'].username)
            GameConsumer.players += 1

            if GameConsumer.players == 2 and self.frame_task is None:
                self.frame_task = asyncio.create_task(self.send_every_frame())
        else:
            await self.close(400)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']
        amIfirst = text_data_json['amIfirst']

        if message == 'move':
            direction = text_data_json['direction']
            await self.calculate_y(direction, amIfirst)
        elif message == 'initial_data':
            await self.setPlayer(amIfirst, text_data_json)

    async def setPlayer(self, amIfirst, text_data_json):
        if amIfirst:
            self.player1 = text_data_json['Player1']
        else:
            self.player2 = text_data_json['Player2']

    async def calculate_y(self, direction, amIfirst):
        y = GameConsumer.player1_y if amIfirst else GameConsumer.player2_y
        increment = 0.01 if 'left' in direction else -0.01
        y += increment
        y = y % (2 * math.pi)
        if amIfirst:
            GameConsumer.player1_y = y
        else:
            GameConsumer.player2_y = y

    async def create_group(self, group_name):
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )

    async def move(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'player1_y': data['player1_y'],
            'player2_y': data['player2_y'],
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name
        )
        GameConsumer.players -= 1
        if self.scope['user'].username in self.player_names:
            self.player_names.remove(self.scope['user'].username)

        # Cancel the frame sending coroutine if a player disconnects
        if GameConsumer.players < 2 and self.frame_task is not None:
            self.frame_task.cancel()
            self.frame_task = None

    async def send_every_frame(self, frame_rate=60):
        frame_duration = 1 / frame_rate
        try:
            while True:
                await self.channel_layer.group_send(
                    self.game_id,
                    {
                        'type': 'move',
                        'data': {
                            'player1_y': GameConsumer.player1_y,
                            'player2_y': GameConsumer.player2_y,
                        }
                    }
                )
                await asyncio.sleep(frame_duration)
        except asyncio.CancelledError:
            pass
