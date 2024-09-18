import json
import random

from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer


class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = []

    async def connect(self):
        await self.create_group(str(self.scope['user'].id))
        await self.accept()
        await self.get_user_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            str(self.scope['user'].id),
            self.channel_name
        )
        if self.scope['user'] in self.queue:
            self.queue.remove(self.scope['user'])
        print('User removed from queue:', self.scope['user'].id)

    async def add_to_game(self):
        if len(self.queue) < 2:
            return
        player1 = self.queue.pop(0)
        player2 = self.queue.pop(0)
        room_id = random.randint(1, 1000)
        print('Creating game with room_id:', room_id)
        await self.channel_layer.group_send(
            str(player1.id),
            {
                'type': 'game_start',
                'data': {
                    'room_id': room_id,
                    'am_i_first': True,
                    'playerId': player1.username,
                    'opponentId': player2.username,
                }
            }
        )
        await self.channel_layer.group_send(
            str(player2.id),
            {
                'type': 'game_start',
                'data': {
                    'room_id': room_id,
                    'am_i_first': False,
                    'playerId': player2.username,
                    'opponentId': player1.username,
                }
            }
        )
        cache.set(f'{room_id}:player1', player1.id)
        cache.set(f'{room_id}:player2', player2.id)
        await self.channel_layer.group_send(
            str(player1.id),
            {
                'type': 'redirect',
            }
        )
        await self.channel_layer.group_send(
            str(player2.id),
            {
                'type': 'redirect',
            }
        )

    async def create_group(self, user):
        await self.channel_layer.group_add(
            user,
            self.channel_name
        )

    async def get_user_data(self):
        user_data = self.scope['user']
        self.queue.append(user_data)
        print('User added to queue:', user_data.username)
        if len(self.queue) >= 2:
            await self.add_to_game()

    async def game_start(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'room_id': data['room_id'],
            'player': data['am_i_first'],
            'playerId': data['playerId'],
            'opponentId': data['opponentId']
        }))

    async def redirect(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
        }))
