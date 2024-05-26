import json
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class MatchmakingConsumer(WebsocketConsumer):
	queue = []

	def connect(self):
		self.create_group(self.scope['user'].username)
		self.accept()
		self.get_user_data()

	def disconnect(self, close_code):
		pass

	def add_to_game(self):
		player1 = self.queue.pop(0)
		player2 = self.queue.pop(0)
		room_id = random.randint(1, 1000)
		print('Creating game with room_id:', room_id)
		async_to_sync(self.channel_layer.group_send)(
			player1.username,
			{
				'type': 'game_start',
				'data': {
					'room_id': room_id,
					'am_i_first': True
				}
			}
		)
		async_to_sync(self.channel_layer.group_send)(
			player2.username,
			{
				'type': 'game_start',
				'data': {
					'room_id': room_id,
					'am_i_first': False
				}
			}
		)
		async_to_sync(self.channel_layer.group_send)(
			player1.username,
			{
				'type': 'redirect',
			}
		)
		async_to_sync(self.channel_layer.group_send)(
			player2.username,
			{
				'type': 'redirect',
			}
		)


	def create_group(self, user):
		async_to_sync(self.channel_layer.group_add)(
			user,
			self.channel_name
		)

	def get_user_data(self):
		user_data = self.scope['user']
		self.queue.append(user_data)
		print('User added to queue:', user_data.username)
		if len(self.queue) >= 2:
			self.add_to_game()

	def game_start(self, event):
		data = event['data']
		self.send(text_data=json.dumps({
			'type': event['type'],
			'room_id': data['room_id'],
			'player': data['am_i_first'],
		}))

	def redirect(self, event):
		self.send(text_data=json.dumps({
			'type': event['type'],
		}))
