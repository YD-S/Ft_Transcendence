import datetime
import hashlib
import json
import os
import random
from urllib.parse import urlencode

import requests
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from NeonPong import settings
from authentication.mail_client import MailClient
from authentication.token import TokenManager, require_token, get_token
from authentication.utils import hash_password
from common.request import HttpRequest
from users.models import User
from users.serializers import UserSerializer
from utils.exception import ValidationError


@require_http_methods(["POST"])
def login_view(request: HttpRequest):
    # Read the username and password from the request
    data = request.json()
    if not data.get('username') or not data.get('password'):
        return HttpResponse(
            json.dumps({"message": "Username and password are required", "type": "login_fail"}),
            content_type='application/json',
            status=400
        )
    # Check if the username and password are correct
    user: User = authenticate(request, username=data.get('username'), password=data.get('password'))
    if user is None:
        return HttpResponse(
            json.dumps({"message": "Invalid username or password", "type": "login_fail"}),
            content_type='application/json',
            status=400
        )
    if user.has_2fa:
        send_2fa_code(user)
        return JsonResponse({
            "action": "2fa",
            "email2fa": user.email,
            "user_id": user.id
        })

    return generate_login(request, user)


def send_2fa_code(user: User):
    user.expected_2fa = random.randint(100000, 999999)
    user.expiration_2fa = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
    user.save()
    mail_client = MailClient()
    mail_client.send_mail(
        mail=user.email,
        subject="2FA",
        reply_to="noreply@neon-pong.com",
        message=f"<p>Tu código de un solo uso es <pre>{user.expected_2fa}</pre></p><p>Caduca en 5 minutos</p>",
        subtype="html"
    )


@require_http_methods(["POST"])
def verify_2fa(request: HttpRequest):
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": "User ID is required", "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    if not data.get('code'):
        return HttpResponse(
            json.dumps({"message": "2FA code is required", "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": "User not found", "type": "2fa_fail"}),
            content_type='application/json',
            status=404
        )
    try:
        code = int(data.get('code'))
    except ValueError:
        return HttpResponse(
            json.dumps({"message": "Invalid 2FA code", "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    if user.expected_2fa != code or user.expiration_2fa < datetime.datetime.now(datetime.UTC):
        return HttpResponse(
            json.dumps({"message": "Invalid 2FA code", "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    user.expected_2fa = None
    user.expiration_2fa = None
    user.save()
    return generate_login(request, user)


def generate_login(request: HttpRequest, user: User):
    try:
        access_token, refresh_token, access_expiration, refresh_expiration = TokenManager().create_token_pair(user.id)
        login(request, user, backend='authentication.backends.TokenBackend')
        return JsonResponse({
            "action": "login",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_expiration": f"{int(access_expiration.timestamp())}",
            "refresh_expiration": f"{int(refresh_expiration.timestamp())}",
        })
    except ValidationError as e:
        return e.as_http_response()


@require_http_methods(["POST"])
def resend_2fa_code(request: HttpRequest):
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": "User ID is required", "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user = User.objects.get(id=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": "User not found", "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    send_2fa_code(user)
    return HttpResponse(
        json.dumps({"message": "2FA code sent"}),
        content_type='application/json',
        status=200
    )


@require_token()
@require_http_methods(["POST"])
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
                "access_expiration": f"{int(access_expiration.timestamp())}",
                "refresh_expiration": f"{int(refresh_expiration.timestamp())}"
            }),
            content_type='application/json',
            status=200
        )
    except ValidationError as e:
        return e.as_http_response()


@require_http_methods(["POST"])
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
    try:
        # Create the user
        User.objects.create_user(
            email=email,
            password=data.get('password'),
            username=username,
        )
    except ValidationError as e:
        return e.as_http_response()
    return HttpResponse(
        json.dumps({"message": "User registered successfully"}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
def change_password(request: HttpRequest):
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
            json.dumps({"message": "User not found", "type": "change_password_fail"}),
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


@require_http_methods(["GET"])
def me(request: HttpRequest):
    return JsonResponse(UserSerializer(instance=request.user).data)


@require_http_methods(["GET"])
def oauth(request: HttpRequest):
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    querystring = urlencode({
        "client_id": settings.CLIENT_ID,
        "redirect_uri": f"{settings.BASE_URL}/auth/oauth_callback",
        "response_type": "code",
        "scope": "public",
        "state": state
    })
    return JsonResponse({"url": f"https://api.intra.42.fr/oauth/authorize?{querystring}", "state": state})


@require_http_methods(["POST"])
def oauth_login(request: HttpRequest):
    data = request.json()
    if not data.get('code'):
        return HttpResponse(
            json.dumps({"message": "Code is required", "type": "oauth_login_fail"}),
            content_type='application/json',
            status=400
        )
    code = data.get('code')
    querystring = urlencode({
        "grant_type": "authorization_code",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": code,
        "redirect_uri": f"{settings.BASE_URL}/auth/oauth_callback"
    })
    response = requests.post(f"https://api.intra.42.fr/oauth/token?{querystring}")
    print(response.status_code)
    if response.status_code != 200:
        return HttpResponse(
            json.dumps({"message": "Invalid code", "type": "oauth_login_fail"}),
            content_type='application/json',
            status=400
        )
    data = response.json()
    user = User.objects.get_or_create_42_user(data)
    return generate_login(request, user)


def send_verification_email(user: User):
    user.email_code = str(hashlib.sha256(os.urandom(1024)).hexdigest())
    user.email_code_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
    user.save()
    mail_client = MailClient()
    mail_client.send_mail(
        mail=user.email,
        subject="2FA",
        reply_to="noreply@neon-pong.com",
        message=f"<p>Haz click en el siguiente enlace para verificar tu correo electrónico: <a href='{settings.BASE_URL}/auth/verify_email?code={user.email_code}'>{settings.BASE_URL}/auth/verify_email?code={user.email_code}</a></p><p>Este enlace caducará en 5 minutos</p>",
        subtype="html"
    )


@require_http_methods(["POST"])
def send_verification_email_view(request: HttpRequest):
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": "User ID is required", "type": "send_verification_email_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user: User = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": "User not found", "type": "send_verification_email_fail"}),
            content_type='application/json',
            status=400
        )
    send_verification_email(user)
    return HttpResponse(
        json.dumps({"message": "Verification email sent"}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
def verify_email(request: HttpRequest):
    data = request.json()
    if not data.get('code'):
        return HttpResponse(
            json.dumps({"message": "Code is required", "type": "verify_email_fail"}),
            content_type='application/json',
            status=400
        )
    code = data.get('code')
    try:
        user = User.objects.get(email_code=code)
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": "Invalid code", "type": "verify_email_fail"}),
            content_type='application/json',
            status=400
        )
    if user.email_code_expiration and user.email_code_expiration < datetime.datetime.now(datetime.UTC):
        return HttpResponse(
            json.dumps({"message": "Code expired", "type": "verify_email_fail"}),
            content_type='application/json',
            status=400
        )
    print("Verified email")
    user.verified_email = True
    user.email_code = None
    user.email_code_expiration = None
    user.save()
    return HttpResponse(
        json.dumps({"message": "Email verified"}),
        content_type='application/json',
        status=200
    )