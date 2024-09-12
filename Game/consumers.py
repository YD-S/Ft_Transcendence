import asyncio
import json
import math
import random
from dataclasses import dataclass
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer

GAME_SIZE = 1000
COURT_RADIUS = 15
PLAYER_WIDTH = GAME_SIZE / 350
BALL_RADIUS = GAME_SIZE / 1500

ANGLE_MARGIN = math.asin((PLAYER_WIDTH + BALL_RADIUS) / 2 / COURT_RADIUS)
BOUNCE_MARGIN = math.pi/6


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

class GameConsumer(AsyncWebsocketConsumer):
    players = 0
    player_names = []
    player1_angle = 0
    player2_angle = math.pi
    last_collision = None
    ball_pos = Vector(0, 0)
    ball_velocity = Vector.from_angle(random.random() * 2 * math.pi)
    ball_speed = 0.1

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

    async def receive(self, text_data: Any | None = None, bytes_data: bytes | None = None):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']
        is_player_first = text_data_json['amIfirst']

        if message == 'move':
            direction = text_data_json['direction']
            await self.calculate_angle(direction, is_player_first)
        elif message == 'initial_data':
            await self.set_player(is_player_first, text_data_json)

    async def calculate_ball_collision(self):
        # Calculate the distance of the ball from the center of the court
        ball_distance = self.ball_pos.magnitude()
        ball_angle = self.ball_velocity.angle()
        # Check if the ball is out of bounds
        if ball_distance > (COURT_RADIUS + BALL_RADIUS):
            if angle_difference(self.player1_angle, ball_angle) < ANGLE_MARGIN:
                await self.bounce(self.player1_angle, 'player1')
            elif angle_difference(self.player2_angle, ball_angle) < ANGLE_MARGIN:
                await self.bounce(self.player2_angle, 'player2')
            else :
                self.reset_ball()
        else:
            GameConsumer.last_collision = None

    async def set_player(self, is_player_first, text_data_json):
        if is_player_first:
            self.player1 = text_data_json['Player1']
        else:
            self.player2 = text_data_json['Player2']

    async def bounce (self, player_angle, player_name):
        with open('bounce.txt', 'a') as f:
            f.write(f'{player_angle}\n')
            f.write(f'{GameConsumer.ball_velocity.angle()}\n')
        await self.channel_layer.group_send(
            self.game_id,
            {
                'type': 'test',
                'data': player_name
            })
        self.ball_velocity = Vector.from_angle(player_angle + (random.random() * BOUNCE_MARGIN - BOUNCE_MARGIN / 2))
        await self.ball_movement()

    async def test(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'test',
            'data': data
        }))

    @staticmethod
    async def calculate_angle(direction, is_player_first):
        a = GameConsumer.player1_angle if is_player_first else GameConsumer.player2_angle
        increment = 0.01 if 'left' in direction else -0.01
        a += increment
        a = a % (2 * math.pi)
        if is_player_first:
            GameConsumer.player1_angle = a
        else:
            GameConsumer.player2_angle = a

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
        }))

    async def disconnect(self, close_code):
        if self.game_id is None:
            return
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
        GameConsumer.player1_angle = 0
        GameConsumer.player2_angle = math.pi
        self.reset_ball()
        try:
            while True:
                await self.ball_movement()
                await self.channel_layer.group_send(
                    self.game_id,
                    {
                        'type': 'move',
                        'data': {
                            'player1_y': GameConsumer.player1_angle,
                            'player2_y': GameConsumer.player2_angle,
                            'ball_x': GameConsumer.ball_pos.x,
                            'ball_y': GameConsumer.ball_pos.y,
                        }
                    }
                )
                await asyncio.sleep(frame_duration)
        except asyncio.CancelledError:
            pass

    async def ball_movement(self):
        if GameConsumer.last_collision is not None:
            #self.reset_ball()
            pass
        else:
            GameConsumer.ball_pos += GameConsumer.ball_velocity * GameConsumer.ball_speed
            await self.calculate_ball_collision()

    @staticmethod
    def reset_ball():
        GameConsumer.last_collision = None
        GameConsumer.ball_pos = Vector(0, 0)
        GameConsumer.ball_velocity = Vector.from_angle(math.pi / 4 * 3)
        GameConsumer.player1_angle = 0
        GameConsumer.player2_angle = math.pi