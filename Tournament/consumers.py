# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        player1 = text_data_json.get('player1')
        player2 = text_data_json.get('player2')
        player3 = text_data_json.get('player3')
        player4 = text_data_json.get('player4')
        semi_winner_1 = text_data_json.get('semi_winner_1')
        semi_winner_2 = text_data_json.get('semi_winner_2')
        final_winner = text_data_json.get('final_winner')

        # Save the tournament asynchronously
        from users.models import Tournament
        await Tournament.objects.acreate(
            player1=player1,
            player2=player2,
            player3=player3,
            player4=player4,
            semi_winner_1=semi_winner_1,
            semi_winner_2=semi_winner_2,
            final_winner=final_winner
        )
