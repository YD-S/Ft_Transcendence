import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from authentication.token import require_token
from chat.models import Message, Room
from chat.serializers import MessageSerializer, RoomSerializer
from common.request import HttpRequest
from users.models import User
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
        try:
            room: Room = Room.objects.get(code=code)
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)
        room.join(request.user)
        room.save()
        return JsonResponse(RoomViewSet.serializer(instance=room).data)

    @staticmethod
    @require_http_methods(["POST"])
    @require_token()
    def leave(request: HttpRequest, pk: int, *args, **kwargs):
        try:
            room: Room = Room.objects.get(id=pk)
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)
        room.leave(request.user)
        room.save()
        return JsonResponse(RoomViewSet.serializer(instance=room).data)

    @staticmethod
    @require_http_methods(["POST"])
    @require_token()
    def direct(request: HttpRequest, username: str, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        room = Room.objects.create(name=f"{request.user.username} - {user.username}", is_direct=True)
        room.join(request.user)
        room.join(user)
        return JsonResponse(RoomViewSet.serializer(instance=room).data)
