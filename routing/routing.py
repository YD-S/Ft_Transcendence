from tkinter.font import names

from django.urls import path, re_path, include
from Game.consumers import GameConsumer
from Matchmaking.consumers import MatchmakingConsumer
from Matchmaking.consumers import GameInviteConsumer
from Tournament.consumers import TournamentConsumer
from chat.consumers import ChatRoomConsumer

websocket_urlpatterns = [
    path('ws/tournament/', TournamentConsumer.as_asgi(), name='tournament'),
    path('ws/matchmaking/', MatchmakingConsumer.as_asgi(), name='matchmaking'),
    path('ws/invite/', GameInviteConsumer.as_asgi(), name='game_invite'),
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatRoomConsumer.as_asgi(), name='chat'),
    re_path(r'ws/game/(?P<game_id>\w+)/$', GameConsumer.as_asgi(), name='game'),
]

apiurls = [
    path('user/', include(("users.urls", "users"), namespace="users")),
    path('auth/', include(("authentication.urls", "authentication"), namespace="authentication")),
    path("chat/", include(("chat.urls", "chat"), namespace="chat")),
]

urlpatterns = [
    path("api/", include(apiurls)),
    path("", include(("website.urls", "website"), namespace="website")),
]
