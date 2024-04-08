from django.shortcuts import render, redirect

from authentication.token import require_token

UNPROTECTED_PAGES = [
    "login"
]


def index(request):
    return redirect("/home")


@require_token
def protected_main_view(request, page):
    return render(request, "index.html", {page: page})


def main_view(request, page):
    if page in UNPROTECTED_PAGES:
        return render(request, "index.html", {"page": page})
    return protected_main_view(request, page)


@require_token
def protected_page_view(request, file):
    match file:
        case "tournament.html":
            return tournament(request)
        case _:
            return render(request, file)


def page_view(request, file):
    if request.headers.get("Sec-Fetch-Mode") == "navigate":
        return redirect("/home")
    page = file.split(".")[0]
    if page in UNPROTECTED_PAGES:
        return render(request, file)
    return protected_page_view(request, file)


def tournament(request):
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
