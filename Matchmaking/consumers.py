import json
import random
from dataclasses import field
from pyexpat.errors import messages

from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse

import logging

log = logging.getLogger(__name__)


class OrderedSet(list):

    def add(self, element):
        if element not in self:
            self.append(element)


class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = OrderedSet()
    private_queue = {}
    sentinel = object()

    async def connect(self):
        if self.scope['user'].id in MatchmakingConsumer.queue:
            return
        await self.create_group(str(self.scope['user'].id))
        await self.accept()
        await self.get_user_data()

    async def disconnect(self, close_code):
        user_id = self.scope['user'].id
        await self.channel_layer.group_discard(
            str(user_id),
            self.channel_name
        )
        log.debug(f'User disconnected: {user_id}')
        if user_id in sum(MatchmakingConsumer.private_queue.values(), OrderedSet()):
            for key in MatchmakingConsumer.private_queue.keys():
                if user_id in MatchmakingConsumer.private_queue[key]:
                    MatchmakingConsumer.private_queue[key].remove(user_id)
                    if not MatchmakingConsumer.private_queue[key]:
                        del MatchmakingConsumer.private_queue[key]
                    break
        elif user_id in MatchmakingConsumer.queue:
            MatchmakingConsumer.queue.remove(user_id)
        log.debug(f'User removed from queue: {user_id}')
        log.debug(f'Queue: {MatchmakingConsumer.queue}, Private Queue: {MatchmakingConsumer.private_queue}')

    async def add_to_game(self, private=False, private_room_id=None):
        from users.models import User
        if (len(MatchmakingConsumer.queue) < 2 and not private) or (private and len(MatchmakingConsumer.private_queue[private_room_id]) < 2):
            return
        player1 = await User.objects.aget(
            id=MatchmakingConsumer.queue.pop(0) if not private else MatchmakingConsumer.private_queue[private_room_id].pop(0))
        player2 = await User.objects.aget(
            id=MatchmakingConsumer.queue.pop(0) if not private else MatchmakingConsumer.private_queue[private_room_id].pop(0))
        cache.delete(f'invite:{player1.id}')
        cache.delete(f'invite:{player2.id}')
        if private:
            del MatchmakingConsumer.private_queue[private_room_id]
        room_id = private_room_id or random.randint(1000, 10000)
        log.debug(f'Creating game with room_id: {room_id}')
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
        user_id = self.scope['user'].id
        log.debug(f'Adding user to queue: {user_id}')
        if (private_room_id := cache.get(f'invite:{user_id}', self.sentinel)) is not self.sentinel:
            MatchmakingConsumer.private_queue[private_room_id] = MatchmakingConsumer.private_queue.get(private_room_id, OrderedSet())
            MatchmakingConsumer.private_queue[private_room_id].add(user_id)
            await self.add_to_game(True, private_room_id)
        else:
            MatchmakingConsumer.queue.add(user_id)
            if len(MatchmakingConsumer.queue) >= 2:
                await self.add_to_game()
        log.debug(f'Queue: {MatchmakingConsumer.queue}, Private Queue: {MatchmakingConsumer.private_queue}')

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
        MatchmakingConsumer.private_queue[private_room_id] = OrderedSet()
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
