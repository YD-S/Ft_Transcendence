import json
import random

from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse


class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = []
    private_queue = {}
    sentinel = object()

    async def connect(self):
        if self.scope['user'] in self.queue:
            self.queue.remove(self.scope['user'])
        await self.create_group(str(self.scope['user'].id))
        await self.accept()
        await self.get_user_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            str(self.scope['user'].id),
            self.channel_name
        )
        if self.scope['user'] in sum(self.private_queue.values(), []):
            for key, value in self.private_queue.items():
                if self.scope['user'] in value:
                    value.remove(self.scope['user'])
                    if not value:
                        del self.private_queue[key]
                    break
        if self.scope['user'] in self.queue:
            self.queue.remove(self.scope['user'])
        print('User removed from queue:', self.scope['user'].id)

    async def add_to_game(self, private=False, private_room_id=None):
        if (len(self.queue) < 2 and not private) or (private and len(MatchmakingConsumer.private_queue[private_room_id]) < 2):
            return
        player1 = self.queue.pop(0) if not private else MatchmakingConsumer.private_queue[private_room_id].pop(0)
        player2 = self.queue.pop(0) if not private else MatchmakingConsumer.private_queue[private_room_id].pop(0)
        cache.delete(f'invite:{player1.id}')
        cache.delete(f'invite:{player2.id}')
        if private:
            del MatchmakingConsumer.private_queue[private_room_id]
        room_id = private_room_id or random.randint(1000, 10000)
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
        if (private_room_id := cache.get(f'invite:{user_data.id}', self.sentinel)) is not self.sentinel:
            MatchmakingConsumer.private_queue[private_room_id] = MatchmakingConsumer.private_queue.get(private_room_id, [])
            MatchmakingConsumer.private_queue[private_room_id].append(self.scope['user'])
            await self.add_to_game(True, private_room_id)
        else:
            self.queue.append(user_data)
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

    @classmethod
    def game_invite(cls, request, *args, **kwargs):
        from users.models import User
        body = json.loads(request.body)
        private_room_id = random.randint(100, 1000)
        user = User.objects.get(id=body['user'])
        cache.set(f'invite:{user.id}', private_room_id)
        cache.set(f'invite:{request.user.id}', private_room_id)
        MatchmakingConsumer.private_queue[private_room_id] = []
        return HttpResponse('')


class GameInviteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            str(self.scope['user'].id),
            {
                'type': 'game_invite',
                'gameSocket': 0,
            }
        )
