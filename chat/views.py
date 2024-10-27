import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from authentication.token import require_token
from chat.models import Message, Room
from chat.serializers import MessageSerializer, RoomSerializer
from common.request import HttpRequest
from utils.modelviewset import ModelViewSet
from users.models import User, BlockedUser, Friendship
from django.utils.translation import gettext as _


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
            return JsonResponse({"error": _("Room not found")}, status=404)
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
            return JsonResponse({"error": _("Room not found")}, status=404)
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
            return JsonResponse({"error": _("User not found")}, status=404)
        if user == request.user:
            return JsonResponse({"error": _("You cannot create a direct room with yourself")}, status=400)
        is_self_blocked = user in [blocked_user.user for blocked_user in BlockedUser.objects.filter(blocked_user=request.user)]
        if is_self_blocked:
            return JsonResponse({"error": _("You are blocked by this user")}, status=401)
        user_is_blocked = user in [blocked_user.blocked_user for blocked_user in BlockedUser.objects.filter(user=request.user)]
        if user_is_blocked:
            return JsonResponse({"error": _("You have blocked this user")}, status=402)
        user_is_friend = user in [friendship.friend for friendship in Friendship.objects.filter(user=request.user)]
        if user_is_friend is False:
            return JsonResponse({"error": _("You are not friends with this user")}, status=403)
        room = Room.objects.create(name=f"{request.user.username} - {user.username}", is_direct=True)
        room.join(request.user)
        room.join(user)
        return JsonResponse(RoomViewSet.serializer(instance=room).data)
