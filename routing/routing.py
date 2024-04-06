from django.urls import path, re_path, include

from chat.consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatRoomConsumer.as_asgi(), name='chat'),
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
