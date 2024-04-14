from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist

from authentication.token import require_token
from chat.models import Room
from chat.serializers import RoomSerializer
from common.request import HttpRequest
from users.serializers import UserSerializer

UNPROTECTED_PAGES = [
    "auth/login",
    "auth/register",
    "auth/2fa",
    "oauth",
    "auth/oauth_callback",
    "auth/verify_email",
]


@require_token()
def protected_main_view(request: HttpRequest, page: str):
    return render(request, "index.html", {"page": page})


def main_view(request: HttpRequest, page: str):
    if page in UNPROTECTED_PAGES:
        return render(request, "index.html", {"page": page})
    return protected_main_view(request, page)


@require_token(login_redirect=False)
def protected_page_view(request: HttpRequest, file: str):
    match file:
        case "me.html":
            return render(request, file, {"user": UserSerializer(instance=request.user).data})
        case "chat.html":
            return chat_view(request)
        case _:
            try:
                return render(request, file)
            except TemplateDoesNotExist:
                return render(request, "404.html")


def page_view(request: HttpRequest, file: str):
    if request.headers.get("Sec-Fetch-Mode") == "navigate":
        return redirect("/home")
    page = file.split(".")[0]
    if page in UNPROTECTED_PAGES:
        return render(request, file)
    return protected_page_view(request, file)


def chat_view(request: HttpRequest):
    rooms = [RoomSerializer(request.user, instance=room).data for room in Room.objects.filter(members__in=[request.user])]
    if "room" in request.GET:
        current_room = Room.objects.filter(members__in=[request.user], id=request.GET["room"])
        if current_room.exists():
            serialized = RoomSerializer(instance=current_room.first()).data
            return render(request, "chat.html", {
                "rooms": rooms,
                "current_room": {**serialized, 'name': current_room.first().get_name(request.user)}
            })
    return render(request, "chat.html", {
        "rooms": rooms
    })
