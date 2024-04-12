from django.http import JsonResponse

from chat.models import Message, Room
from chat.serializers import MessageSerializer, RoomSerializer
from common.request import HttpRequest
from utils.modelviewset import ModelViewSet


class MessageViewSet(ModelViewSet):
    model = Message
    serializer = MessageSerializer


class RoomViewSet(ModelViewSet):
    model = Room
    serializer = RoomSerializer

    def join(self, request: HttpRequest, pk: int, *args, **kwargs):
        room = self.get_instance(pk)
        room.join(request.user)
        return JsonResponse(self.serializer(instance=room).data)
