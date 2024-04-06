from django.shortcuts import render, redirect


def fetch_redirect(file):
    def decorator(func):
        def view(request):
            if request.headers.get("Sec-Fetch-Mode") == "navigate":
                return render(request, "index.html", {"page": file.split(".")[0]})
            return func(request)

        return view

    return decorator


# Index redirects to home
def index(request):
    return redirect("home")


def generic(file: str):
    @fetch_redirect(file)
    def view(request):
        return render(request, file)

    return view


@fetch_redirect("tournament.html")
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
