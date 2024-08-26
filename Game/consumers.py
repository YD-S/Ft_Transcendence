import asyncio
import json
import math
import random

from channels.generic.websocket import AsyncWebsocketConsumer

GAME_SIZE = 1000
COURT_RADIUS = 15
PLAYER_WIDTH = GAME_SIZE / 350
BALL_RADIUS = GAME_SIZE / 1500

class Vector:
    def __init__(self, x, y):
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
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

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

    def project(self, other):
        return other * (self.dot(other) / other.magnitude() ** 2)

    def reflect(self, normal):
        return self - normal * 2 * self.dot(normal)

    def bounce(self, normal):
        return self.reflect(normal).normalize()

    def to_tuple(self):
        return self.x, self.y

    def to_list(self):
        return [self.x, self.y]

    @staticmethod
    def from_angle(angle):
        return Vector(math.cos(angle), math.sin(angle))


class GameConsumer(AsyncWebsocketConsumer):
    players = 0
    player_names = []
    player1_angle = math.pi / 2
    player2_angle = -math.pi / 2
    last_collision = None
    ball_pos = Vector(0, 0)
    ball_velocity = Vector.from_angle(random.random() * 2 * math.pi).normalize()
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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']
        amIfirst = text_data_json['amIfirst']

        if message == 'move':
            direction = text_data_json['direction']
            await self.calculate_y(direction, amIfirst)
        elif message == 'initial_data':
            await self.setPlayer(amIfirst, text_data_json)

    async def calculate_ball_collision(self):
        # difference between vector angles < angle span from center to paddle edges
        ball_distance = self.ball_pos.magnitude()

        margin = Vector(BALL_RADIUS + PLAYER_WIDTH / 2, COURT_RADIUS).angle()
        diff1 = abs(self.ball_pos.angle() - GameConsumer.player1_angle)
        diff2 = abs(self.ball_pos.angle() - GameConsumer.player2_angle)

        print(f'diff1: {diff1} {margin} {diff1 < margin}')
        print(f'diff1: {diff2} {margin} {diff2 < margin}')
        if ball_distance > COURT_RADIUS + 1:
            print("OUT OF BOUNDS")
            if diff1 < margin:
                GameConsumer.last_collision = self.player1
                print("COLLISION PLAYER 1")
            elif diff2 < margin:
                GameConsumer.last_collision = self.player2
                print("COLLISION PLAYER 2")
            self.reset_ball()
        else:
            GameConsumer.last_collision = None

    async def setPlayer(self, amIfirst, text_data_json):
        if amIfirst:
            self.player1 = text_data_json['Player1']
        else:
            self.player2 = text_data_json['Player2']

    async def calculate_y(self, direction, amIfirst):
        y = GameConsumer.player1_angle if amIfirst else GameConsumer.player2_angle
        increment = 0.01 if 'left' in direction else -0.01
        y += increment
        y = y % (2 * math.pi)
        if amIfirst:
            GameConsumer.player1_angle = y
        else:
            GameConsumer.player2_angle = y

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
        GameConsumer.player1_angle = math.pi / 2
        GameConsumer.player2_angle = -math.pi / 2
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
            self.reset_ball()
        else:
            GameConsumer.ball_pos += GameConsumer.ball_velocity * GameConsumer.ball_speed
            await self.calculate_ball_collision()

    def reset_ball(self):
        GameConsumer.last_collision = None
        GameConsumer.ball_pos = Vector(0, 0)
        GameConsumer.ball_velocity = Vector.from_angle(random.random() * 2 * math.pi).normalize()
