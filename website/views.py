from django.shortcuts import render, redirect

from authentication.token import require_token
from common.request import HttpRequest
from users.serializers import UserSerializer

UNPROTECTED_PAGES = [
    "login",
    "register",
    "2fa",
    "oauth",
    "oauth_callback",
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
    return render(request, "tournament.html", {
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

