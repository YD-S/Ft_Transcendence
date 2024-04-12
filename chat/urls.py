from django.urls.conf import path

from chat import views

urlpatterns = [
    path('message/', views.MessageViewSet.as_view(), name='message'),
    path('message/<int:pk>', views.MessageViewSet.as_view(True), name='message'),
    path('room/', views.RoomViewSet.as_view(), name='room'),
    path('room/<int:pk>', views.RoomViewSet.as_view(True), name='room'),
]
