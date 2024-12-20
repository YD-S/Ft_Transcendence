import logging
from pprint import pprint

from django.contrib.auth import login
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist

from authentication.token import require_token
from chat.models import Room
from chat.serializers import RoomSerializer
from common.request import HttpRequest
from users.forms import UserForm
from users.models import User, BlockedUser, Friendship, Match
from utils.exception import NotFoundError, HttpError

UNPROTECTED_PAGES = [
    "auth/login",
    "auth/register",
    "auth/2fa",
    "oauth",
    "auth/oauth_callback",
    "auth/verify_email",
]

log = logging.getLogger(__name__)


def upload_avatar(file, user: User):
    with open(f'/media/avatars/{user.username}.{file.name.split(".")[-1]}', "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def handle_post(request: HttpRequest, page: str):
    match page:
        case 'edit-profile':
            if request.user.is_anonymous:
                return redirect("/auth/login")
            form = UserForm(data=request.POST, files=request.FILES, instance=request.user)

            if form.is_valid():
                user = form.save()
                login(request, user, backend='authentication.backends.TokenBackend')
                return JsonResponse({"message": "Avatar updated", "success": True})

    raise NotFoundError()


@require_token()
def protected_main_view(request: HttpRequest, page: str):
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
    match file:
        case "friendlist.html":
            friends = [
                          {
                              'id': friendship.id,
                              'user': friendship.friend
                          }
                          for friendship in Friendship.objects.filter(
                    Q(user_id=request.GET.get('user', request.user.id))
                )
                      ] + [
                          {
                              'id': friendship.id,
                              'user': friendship.user
                          }
                          for friendship in Friendship.objects.filter(
                    Q(friend_id=request.GET.get('user', request.user.id))
                )
                      ]
            return render(request, file, {"friends": friends})
        case "me.html":
            return render(request, file, {"user": request.user, "stats": calculate_stats(request.user)})
        case "user.html":
            try:
                return user_page(request)
            except User.DoesNotExist:
                return render(request, "404.html")
        case "chat.html":
            return chat_view(request)
        case "room.html":
            return room_view(request)
        case "edit-profile.html":
            return render(request, file, {"form": UserForm()})
        case _:
            try:
                return render(request, file)
            except TemplateDoesNotExist:
                return render(request, "404.html")


def calculate_stats(user: User):
    wins = Match.objects.filter(winner=user).count()
    losses = Match.objects.filter(loser=user).count()
    match_count = wins + losses
    winrate = (wins / match_count) if match_count != 0 else 0
    return {
        "friends": Friendship.objects.filter(user=user).count() + Friendship.objects.filter(friend=user).count(),
        "match_count": match_count,
        "winrate": f'{winrate * 100:.2f}%' if winrate != 0 else "0.00%",
        "wins": wins,
        "losses": losses,
        "matches": [
            {
                "opponent": (match.loser if match.winner == user else match.winner).username,
                "opponent_id": (match.loser if match.winner == user else match.winner).id,
                "result": "win" if match.winner == user else "loss",
                "score": f"{match.winner_score} - {match.loser_score}" if match.winner == user else f"{match.loser_score} - {match.winner_score}",
                "date": match.date
            }
            for match in Match.objects.filter(Q(winner=user) | Q(loser=user))
        ]
    }


def user_page(request):
    user = User.objects.get(id=int(request.GET.get('id', 0)))
    is_self_blocked = user in [blocked_user.user for blocked_user in BlockedUser.objects.filter(blocked_user=request.user)]
    if is_self_blocked:
        return render(request, "404.html")
    user_is_blocked = user in [blocked_user.blocked_user for blocked_user in BlockedUser.objects.filter(user=request.user)]
    user_is_friend = user in [friendship.friend for friendship in Friendship.objects.filter(user=request.user)] + [friendship.user for friendship in
                                                                                                                   Friendship.objects.filter(
                                                                                                                       friend=request.user)]
    if user_is_blocked:
        block = BlockedUser.objects.filter(user=request.user).get(blocked_user=user)
    else:
        block = None
    if user_is_friend:
        try:
            friend = Friendship.objects.filter(user=request.user).get(friend=user)
        except Friendship.DoesNotExist:
            try:
                friend = Friendship.objects.filter(friend=request.user).get(user=user)
            except Friendship.DoesNotExist:
                friend = None
    else:
        friend = None
    if user == request.user:
        return render(request, "me.html", {"user": request.user})
    sentinel = object()
    stats = calculate_stats(user)
    return render(request, "user.html", {
        "user": user,
        "online": cache.get(f"user:{user.id}:token", sentinel) is not sentinel,
        "is_not_blocked": not user_is_blocked,
        "block": block,
        "is_not_friend": not user_is_friend,
        "friend": friend,
        "stats": stats
    })


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
        room: Room = current_room.first()
        return render(request, "room.html", {
            "current_room": RoomSerializer(request.user, instance=room).data,
            "user_id": room.members.filter(~Q(id=request.user.id)).first().id if room.is_direct else None
        })
    return render(request, "room.html")
