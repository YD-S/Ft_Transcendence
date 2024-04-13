import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from authentication.token import require_token
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

    def post(self, request: HttpRequest, *args, **kwargs):
        resp: JsonResponse = super().post(request, *args, **kwargs)
        instance = Room.objects.get(id=json.loads(resp.content)['id'])
        instance.join(request.user)
        instance.save()
        return resp

    @staticmethod
    @require_http_methods(["POST"])
    @require_token()
    def join(request: HttpRequest, code: str, *args, **kwargs):
        instance: Room = Room.objects.get(code=code)
        instance.join(request.user)
        instance.save()
        return JsonResponse(RoomViewSet.serializer(instance=instance).data)

    @staticmethod
    @require_http_methods(["POST"])
    @require_token()
    def leave(request: HttpRequest, pk: int, *args, **kwargs):
        instance: Room = Room.objects.get(id=pk)
        instance.leave(request.user)
        instance.save()
        return JsonResponse(RoomViewSet.serializer(instance=instance).data)
