from django.shortcuts import render, redirect

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
        case "tournament.html":
            return tournament(request)
        case "me.html":
            return render(request, file, {"user": UserSerializer(instance=request.user).data})
        case "chat.html":
            return chat_view(request)
        case _:
            return render(request, file)


def page_view(request: HttpRequest, file: str):
    if request.headers.get("Sec-Fetch-Mode") == "navigate":
        return redirect("/home")
    page = file.split(".")[0]
    if page in UNPROTECTED_PAGES:
        return render(request, file)
    return protected_page_view(request, file)


def tournament(request: HttpRequest):
    spacing = 4.7
    return render(request, "pong/tournament.html", {
        "tournament": {
            "name": "Tournament Name",
            "final": {
                "player1": "Player",
                "player2": "Player",
            },
            "rounds_left": [
                {
                    "round": 0 * spacing,
                    "name": "Round 1",
                    "matches": [
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                    ],
                },
                {
                    "round": 1 * spacing,
                    "name": "Round 2",
                    "matches": [
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                    ],
                },
                {
                    "round": 3 * spacing,
                    "name": "Round 3",
                    "matches": [
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                    ],
                },
            ],
            "rounds_right": [
                {
                    "round": 0 * spacing,
                    "name": "Round 1",
                    "matches": [
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                    ],
                },
                {
                    "round": 1 * spacing,
                    "name": "Round 2",
                    "matches": [
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                    ],
                },
                {
                    "round": 2 * spacing,
                    "name": "Round 3",
                    "matches": [
                        {
                            "player1": "Player",
                            "player2": "Player",
                            "score1": 0,
                            "score2": 0,
                        },
                    ],
                },
            ],
        },
    })


def chat_view(request: HttpRequest):
    def get_rooms(is_direct: bool):
        return [RoomSerializer(request.user, instance=room).data for room in
                Room.objects.filter(members__in=[request.user], is_direct=is_direct)]

    group_rooms = get_rooms(False)
    direct_rooms = get_rooms(True)
    if "room" in request.GET:
        current_room = Room.objects.filter(members__in=[request.user], id=request.GET["room"])
        if current_room.exists():
            serialized = RoomSerializer(instance=current_room.first()).data
            return render(request, "chat.html", {
                "group_rooms": group_rooms,
                "direct_rooms": direct_rooms,
                "current_room": {**serialized, 'name': current_room.first().get_name(request.user)}
            })
    return render(request, "chat.html", {
        "group_rooms": group_rooms,
        "direct_rooms": direct_rooms
    })
