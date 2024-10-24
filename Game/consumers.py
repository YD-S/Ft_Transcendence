import asyncio
import json
import math
import random
from dataclasses import dataclass
from typing import Any, Dict

from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer

GAME_SIZE = 1000
COURT_RADIUS = 15
PLAYER_WIDTH = GAME_SIZE / 350
BALL_RADIUS = GAME_SIZE / 1500
WINNING_SCORE = 2

ANGLE_MARGIN = math.asin((PLAYER_WIDTH / 2 + BALL_RADIUS) / COURT_RADIUS)
BOUNCE_MARGIN = math.pi / 3


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return f"({self.x:.5f}, {self.y:.5f})"

    def __repr__(self):
        return str(self)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        return self / self.magnitude()

    def angle(self):
        return math.atan2(self.y, self.x)

    def rotate(self, angle: float):
        """
        Rotate the vector by a given angle in radians
        :param angle: The angle in radians
        """
        return Vector(self.x * math.cos(angle) - self.y * math.sin(angle),
                      self.x * math.sin(angle) + self.y * math.cos(angle))

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    @staticmethod
    def from_angle(angle):
        return Vector(math.cos(angle), math.sin(angle))


def angle_difference(angle1: float, angle2: float):
    return min([
        abs(angle1 - angle2),
        abs(angle1 - angle2 + 2 * math.pi),
        abs(angle1 - angle2 - 2 * math.pi),
    ])

@dataclass
class GameState:
    player1_angle: float = 0
    player2_angle: float = math.pi
    player1_score: int = 0
    player2_score: int = 0
    ball_pos: Vector = Vector(0, 0)
    ball_velocity: Vector = Vector(0, 0)
    last_collision: str = None
    game_finished: bool = False

class GameConsumer(AsyncWebsocketConsumer):
    sockets = {}
    games: Dict[int, GameState] = {}
    players : Dict[int, int] = {}
    player_names = []
    ball_speed = 0.18

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player1 = None
        self.player2 = None
        self.game_id = None
        self.frame_task = None  # Task to manage the frame sending coroutine

    async def connect(self):
        await self.accept()
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        if GameConsumer.players.get(self.game_id, 0) < 2:
            GameConsumer.players[self.game_id] = GameConsumer.players.get(self.game_id, 0) + 1
            await self.create_group(self.game_id)
            self.player_names.append(self.scope['user'].username)
            cache.set(f'{self.game_id}:player1' if GameConsumer.players[self.game_id] == 0 else f'{self.game_id}:player2', self.scope['user'].id)
            if self.game_id not in GameConsumer.sockets:
                GameConsumer.sockets[self.game_id] = [self]
            else:
                GameConsumer.sockets[self.game_id].append(self)
            if GameConsumer.players[self.game_id] == 2 and self.frame_task is None:
                GameConsumer.games[self.game_id] = GameState()
                self.frame_task = asyncio.create_task(self.send_every_frame())
        else:
            await self.close(reason='Game is full')

    async def receive(self, text_data: Any | None = None, bytes_data: bytes | None = None):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']

        if message == 'move':
            is_player_first = text_data_json['amIfirst']
            direction = text_data_json['direction']
            await self.calculate_angle(direction, is_player_first)
        if message == 'leave':
            from users.models import User
            player_id = text_data_json['playerId']
            p1 = cache.get(f'{self.game_id}:player1')
            p2 = cache.get(f'{self.game_id}:player2')
            p1_obj, p2_obj = await User.objects.aget(id=p1), await User.objects.aget(id=p2)
            if player_id == p1_obj.username:
                GameConsumer.player2_score = WINNING_SCORE
            elif player_id == p2_obj.username:
                GameConsumer.player1_score = WINNING_SCORE

    async def calculate_ball_collision(self):
        # Calculate the distance of the ball from the center of the court
        ball_distance = GameConsumer.games[self.game_id].ball_pos.magnitude()
        ball_angle = GameConsumer.games[self.game_id].ball_pos.angle()
        # Check if the ball is out of bounds
        if ball_distance > (COURT_RADIUS - BALL_RADIUS):
            if angle_difference(GameConsumer.games[self.game_id].player1_angle, ball_angle) < ANGLE_MARGIN:
                await self.bounce(GameConsumer.games[self.game_id].player1_angle, 'player1')
            elif angle_difference(GameConsumer.games[self.game_id].player2_angle, ball_angle) < ANGLE_MARGIN:
                await self.bounce(GameConsumer.games[self.game_id].player2_angle, 'player2')
            else:
                self.add_score()
                self.reset_ball()

    async def bounce(self, player_angle, player_name):
        GameConsumer.games[self.game_id].last_collision = player_name
        GameConsumer.games[self.game_id].ball_velocity = - Vector.from_angle(
            player_angle + (random.random() * BOUNCE_MARGIN - BOUNCE_MARGIN / 2))
        GameConsumer.games[self.game_id].ball_pos = GameConsumer.games[self.game_id].ball_pos.normalize() * ((COURT_RADIUS - BALL_RADIUS) * 0.98)

    async def calculate_angle(self, direction, is_player_first):
        a = GameConsumer.games[self.game_id].player1_angle if is_player_first else GameConsumer.games[self.game_id].player2_angle
        increment = 0.01 if 'left' in direction else -0.01
        a += increment
        a = a % (2 * math.pi)
        if is_player_first:
            GameConsumer.games[self.game_id].player1_angle = a
        else:
            GameConsumer.games[self.game_id].player2_angle = a

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
            'ball_x': data['ball_x'],
            'ball_y': data['ball_y'],
            'player1_score': GameConsumer.games[self.game_id].player1_score,
            'player2_score': GameConsumer.games[self.game_id].player2_score,
            'last_collision': GameConsumer.games[self.game_id].last_collision
        }))

    async def disconnect(self, close_code):
        if self.game_id is None:
            return
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name
        )
        GameConsumer.players[self.game_id] -= 1
        if self.scope['user'].username in self.player_names:
            GameConsumer.player_names.remove(self.scope['user'].username)

        # Cancel the frame sending coroutine if a player disconnects
        if GameConsumer.players[self.game_id] < 2 and self.frame_task is not None:
            self.frame_task.cancel()
            self.frame_task = None
            for socket in GameConsumer.sockets[self.game_id]:
                try:
                    await socket.close(reason='Game Finished')
                    del GameConsumer.sockets[self.game_id]
                except:
                    pass

    async def send_every_frame(self, frame_rate=60):
        frame_duration = 1 / frame_rate
        GameConsumer.games[self.game_id].player1_angle = 0
        GameConsumer.games[self.game_id].player2_angle = math.pi
        self.reset_ball()
        try:
            while True:
                await self.check_winner()
                await self.ball_movement()
                await self.channel_layer.group_send(
                    self.game_id,
                    {
                        'type': 'move',
                        'data': {
                            'player1_y': GameConsumer.games[self.game_id].player1_angle,
                            'player2_y': GameConsumer.games[self.game_id].player2_angle,
                            'ball_x': GameConsumer.games[self.game_id].ball_pos.x,
                            'ball_y': GameConsumer.games[self.game_id].ball_pos.y,
                        }
                    }
                )
                await asyncio.sleep(frame_duration)
        except asyncio.CancelledError:
            pass

    async def ball_movement(self):
        GameConsumer.games[self.game_id].ball_pos += GameConsumer.games[self.game_id].ball_velocity * GameConsumer.ball_speed
        await self.calculate_ball_collision()

    def reset_ball(self):
        GameConsumer.games[self.game_id].last_collision = None
        GameConsumer.games[self.game_id].ball_pos = Vector(0, 0)
        GameConsumer.games[self.game_id].ball_velocity = Vector.from_angle(math.pi / 4 * 3)
        GameConsumer.games[self.game_id].player1_angle = 0
        GameConsumer.games[self.game_id].player2_angle = math.pi


    def add_score(self):
        if GameConsumer.games[self.game_id].last_collision == 'player1':
            GameConsumer.games[self.game_id].player1_score += 1
        elif GameConsumer.games[self.game_id].last_collision == 'player2':
            GameConsumer.games[self.game_id].player2_score += 1

    async def check_winner(self):
        if GameConsumer.games[self.game_id].player1_score == WINNING_SCORE:
            await self.send_winner_message(cache.get(f'{self.game_id}:player1'), cache.get(f'{self.game_id}:player2'),
                                           GameConsumer.games[self.game_id].player1_score,
                                           GameConsumer.games[self.game_id].player2_score)
        elif GameConsumer.games[self.game_id].player2_score == WINNING_SCORE:
            await self.send_winner_message(cache.get(f'{self.game_id}:player2'), cache.get(f'{self.game_id}:player1'),
                                           GameConsumer.games[self.game_id].player2_score,
                                           GameConsumer.games[self.game_id].player1_score)

    async def winner(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'winner',
            **data
        }))

    async def send_winner_message(self, winner: int, looser: int, winner_score: int, looser_score: int):

        if not GameConsumer.games[self.game_id].game_finished:
            from users.models import User, Match
            winner_obj = await User.objects.aget(id=winner)
            looser_obj = await User.objects.aget(id=looser)
            cache.delete(f'{self.game_id}:player1')
            cache.delete(f'{self.game_id}:player2')
            GameConsumer.games[self.game_id].game_finished = True
            GameConsumer.games[self.game_id].player1_score = 0
            GameConsumer.games[self.game_id].player2_score = 0
            GameConsumer.games[self.game_id].player_names = []
            await Match.objects.acreate(winner=winner_obj, loser=looser_obj, winner_score=winner_score,
                                        loser_score=looser_score)
            await self.channel_layer.group_send(
                self.game_id,
                {
                    'type': 'winner',
                    'data': {
                        'winner': winner_obj.username
                    }
                }
            )
