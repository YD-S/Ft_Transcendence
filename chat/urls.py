from django.urls.conf import path

from chat import views

urlpatterns = [
    path('message/', views.MessageViewSet.as_view(), name='message'),
    path('message/<int:pk>', views.MessageViewSet.as_view(True), name='message'),
    path('room/', views.RoomViewSet.as_view(), name='room'),
    path('room/join/<str:code>', views.RoomViewSet.join, name='room_join'),
    path('room/leave/<int:pk>', views.RoomViewSet.leave, name='room_leave'),
    path('room/direct/<str:username>', views.RoomViewSet.direct, name='room_direct'),
    path('room/<int:pk>', views.RoomViewSet.as_view(True), name='room'),
]
