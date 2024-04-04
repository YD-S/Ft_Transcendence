import json

from django.db.models import QuerySet
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from authentication.token import TokenManager, require_token, get_token
from authentication.utils import hash_password
from common.request import HttpRequest, wrap_funcview
from users.models import User
from users.serializers import UserSerializer
from utils.exception import ValidationError


@require_http_methods(["POST"])
@wrap_funcview
def login(request):
    # Read the username and password from the request
    data = request.json()
    if not data.get('username') or not data.get('password'):
        return HttpResponse(
            json.dumps({"message": "Username and password are required", "type": "login_fail"}),
            content_type='application/json',
            status=400
        )
    username = data.get('username')
    password_hash = hash_password(data.get('password'))
    # Check if the username and password are correct
    user: QuerySet[User] = User.objects.filter(username=username)
    if not user.exists():
        return HttpResponse(
            json.dumps({"message": f"User or password incorrect", "type": "login_fail"}),
            content_type='application/json',
            status=400
        )
    user: User = user.first()
    # Check the hash
    if user.password != password_hash:
        return HttpResponse(
            json.dumps({"message": f"User or password incorrect", "type": "login_fail"}),
            content_type='application/json',
            status=400
        )

    # Create JWT token
    try:
        access_token, refresh_token, access_expiration, refresh_expiration = TokenManager().create_token_pair(user.id)
        return HttpResponse(
            json.dumps({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_expiration": f"{access_expiration:%Y-%m-%d %H:%M:%S}",
                "refresh_expiration": f"{refresh_expiration:%Y-%m-%d %H:%M:%S}"
            }),
            content_type='application/json',
            status=200
        )
    except ValidationError as e:
        return e.as_http_response()


@require_http_methods(["POST"])
@require_token
@wrap_funcview
def logout(request: HttpRequest):
    try:
        TokenManager().revoke_token(get_token(request))
    except ValidationError as e:
        return e.as_http_response()
    return HttpResponse(
        json.dumps({"message": "Logout successful"}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
@wrap_funcview
def refresh(request: HttpRequest):
    # Read the token from the header
    data = request.json()
    if not data.get('refresh_token'):
        return HttpResponse(
            json.dumps({"message": "Refresh token is required", "type": "refresh_fail"}),
            content_type='application/json',
            status=400
        )
    refresh_token = data.get('refresh_token')
    # Refresh the token
    try:
        access_token, refresh_token, access_expiration, refresh_expiration = TokenManager().refresh_token(refresh_token)
        return HttpResponse(
            json.dumps({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_expiration": f"{access_expiration:%Y-%m-%d %H:%M:%S}",
                "refresh_expiration": f"{refresh_expiration:%Y-%m-%d %H:%M:%S}"
            }),
            content_type='application/json',
            status=200
        )
    except ValidationError as e:
        return e.as_http_response()


@require_http_methods(["POST"])
@wrap_funcview
def register(request: HttpRequest):
    # Read the username and password from the request
    data = request.json()
    if not data.get('username') or not data.get('password') or not data.get('email'):
        return HttpResponse(
            json.dumps({"message": "Username and password and email are required", "type": "register_fail"}),
            content_type='application/json',
            status=400
        )
    username = data.get('username')
    email = data.get('email')
    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return HttpResponse(
            json.dumps({"message": "Username already exists", "type": "register_fail"}),
            content_type='application/json',
            status=400
        )
    # Create the user
    user = UserSerializer(data={
        "username": username,
        "email": email,
        "password": data.get('password')
    })
    try:
        user.save()
    except ValidationError as e:
        return e.as_http_response()
    return HttpResponse(
        json.dumps({"message": "User registered successfully"}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
@wrap_funcview
def change_password(request):
    # Read the passwords from the request
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": "User ID is required", "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    if not data.get('current_password'):
        return HttpResponse(
            json.dumps({"message": "Current password is required", "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    if not data.get('new_password'):
        return HttpResponse(
            json.dumps({"message": "New password is required", "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": "User does found", "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    current_password = hash_password(data.get('current_password'))
    if user.password != current_password:
        return HttpResponse(
            json.dumps({"message": "Current password is incorrect", "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    new_password = hash_password(data.get('new_password'))
    if new_password == current_password:
        return HttpResponse(
            json.dumps({"message": "New password must be different from current password", "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    user.password = new_password
    user.save()
    return HttpResponse(
        json.dumps({"message": "Password changed successfully"}),
        content_type='application/json',
        status=200
    )
