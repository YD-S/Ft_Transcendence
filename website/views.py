from pprint import pprint

from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist

from authentication.token import require_token
from chat.models import Room
from chat.serializers import RoomSerializer
from common.request import HttpRequest
from users.forms import UserForm
from users.models import User, BlockedUser, Friendship
from utils.exception import NotFoundError, HttpError

UNPROTECTED_PAGES = [
    "auth/login",
    "auth/register",
    "auth/2fa",
    "oauth",
    "auth/oauth_callback",
    "auth/verify_email",
]


def handle_post(request: HttpRequest, page: str):
    match page:
        case 'edit-profile':
            form = UserForm(data=request.POST, files=request.FILES, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect("/me")

    raise NotFoundError()


@require_token()
def protected_main_view(request: HttpRequest, page: str):
    print("r:", request.method, request.FILES)
    if request.method == 'POST':
        return handle_post(request, page)
    if request.method == 'GET':
        return render(request, "index.html", {"page": page})


def main_view(request: HttpRequest, page: str):
    try:
        if page in UNPROTECTED_PAGES:
            return render(request, "index.html", {"page": page})
        return protected_main_view(request, page)
    except HttpError as e:
        return e.as_http_response(True)


@require_token(login_redirect=False)
def protected_page_view(request: HttpRequest, file: str):
    print(file)
    match file:
        case "me.html":
            return render(request, file, {"user": request.user})
        case "user.html":
            try:
                user = User.objects.get(id=int(request.GET.get('id', 0)))
                user_is_blocked = user in [blocked_user.blocked_user for blocked_user in BlockedUser.objects.filter(user=request.user)]
                user_is_friend = user in [friendship.friend for friendship in Friendship.objects.filter(user=request.user)]
                if user_is_blocked:
                    block = BlockedUser.objects.filter(user=request.user).get(blocked_user=user)
                else:
                    block = None
                if user_is_friend:
                    friend = Friendship.objects.filter(user=request.user).get(friend=user)
                else:
                    friend = None
                return render(request, "users.html", {
                    "user": user,
                    "is_not_blocked": not user_is_blocked,
                    "block": block,
                    "is_not_friend": not user_is_friend,
                    "friend": friend
                })
            except User.DoesNotExist:
                return render(request, "404.html")
        case "chat.html":
            return chat_view(request)
        case "room.html":
            return room_view(request)
        case "edit-profile.html":
            return render(request, file, {"form": UserForm(instance=request.user)})
        case _:
            try:
                return render(request, file)
            except TemplateDoesNotExist:
                return render(request, "404.html")


def page_view(request: HttpRequest, file: str):
    try:
        if request.headers.get("Sec-Fetch-Mode") == "navigate":
            return redirect("/home")
        page = file.split(".")[0]
        if page in UNPROTECTED_PAGES:
            return render(request, file)
        return protected_page_view(request, file)
    except HttpError as e:
        return e.as_http_response()


def chat_view(request: HttpRequest):
    rooms = [RoomSerializer(request.user, instance=room).data for room in Room.objects.filter(members__in=[request.user])]
    return render(request, "chat.html", {
        "rooms": rooms
    })


def room_view(request: HttpRequest):
    current_room = Room.objects.filter(members__in=[request.user], id=request.GET.get("room", 0))
    if current_room.exists():
        d = RoomSerializer(request.user, instance=current_room.first()).data
        pprint(d)
        return render(request, "room.html", {
            "current_room": d
        })
    return render(request, "room.html")
