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
from django.core.cache import cache

from django.utils.translation import gettext as _


@require_http_methods(["POST"])
def login_view(request: HttpRequest):
    # Read the username and password from the request
    data = request.json()
    if not data.get('username') or not data.get('password'):
        return HttpResponse(
            json.dumps({"message": _("Username and password are required"), "type": "login_fail"}),
            content_type='application/json',
            status=400
        )
    # Check if the username and password are correct
    user: User = authenticate(request, username=data.get('username'), password=data.get('password'))
    if user is None:
        return HttpResponse(
            json.dumps({"message": _("Invalid username or password"), "type": "login_fail"}),
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
    expected_2fa = random.randint(100000, 999999)
    cache.set(f'{user.id}_2fa', expected_2fa, timeout=300)
    mail_client = MailClient()
    mail_client.send_mail(
        mail=user.email,
        subject=_("Two-Factor Authentication"),
        reply_to="noreply@neon-pong.com",
        message="<p>" + _("Your one-time passcode is") + f"<pre>{expected_2fa}</pre></p><p>" + _("It expires in 5 minutes") + "</p>",
        subtype="html"
    )


@require_http_methods(["POST"])
def verify_2fa(request: HttpRequest):
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": _("User ID is required"), "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    if not data.get('code'):
        return HttpResponse(
            json.dumps({"message": _("2FA code is required"), "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": _("User not found"), "type": "2fa_fail"}),
            content_type='application/json',
            status=404
        )
    try:
        code = int(data.get('code'))
    except ValueError:
        return HttpResponse(
            json.dumps({"message": _("Invalid 2FA code"), "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    sentinel = object()
    expected_2fa = cache.get(f'{user.id}_2fa', sentinel)
    if expected_2fa is sentinel or expected_2fa != code:
        return HttpResponse(
            json.dumps({"message": _("Invalid 2FA code"), "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    cache.delete(f'{user.id}_2fa')
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
            json.dumps({"message": _("User ID is required"), "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user = User.objects.get(id=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": _("User not found"), "type": "2fa_fail"}),
            content_type='application/json',
            status=400
        )
    send_2fa_code(user)
    return HttpResponse(
        json.dumps({"message": _("2FA code sent")}),
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
        json.dumps({"message": _("Logout successful")}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
def refresh(request: HttpRequest):
    # Read the token from the header
    data = request.json()
    if not data.get('refresh_token'):
        return HttpResponse(
            json.dumps({"message": _("Refresh token is required"), "type": "refresh_fail"}),
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
            json.dumps({"message": _("Username and password and email are required"), "type": "register_fail"}),
            content_type='application/json',
            status=400
        )
    username = data.get('username')
    email = data.get('email')
    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return HttpResponse(
            json.dumps({"message": _("Username already exists"), "type": "register_fail"}),
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
        json.dumps({"message": _("User registered successfully")}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
def change_password(request: HttpRequest):
    # Read the passwords from the request
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": _("User ID is required"), "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    if not data.get('current_password'):
        return HttpResponse(
            json.dumps({"message": _("Current password is required"), "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    if not data.get('new_password'):
        return HttpResponse(
            json.dumps({"message": _("New password is required"), "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": _("User not found"), "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    current_password = hash_password(data.get('current_password'))
    if user.password != current_password:
        return HttpResponse(
            json.dumps({"message": _("Current password is incorrect"), "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    new_password = hash_password(data.get('new_password'))
    if new_password == current_password:
        return HttpResponse(
            json.dumps({"message": _("New password must be different from current password"), "type": "change_password_fail"}),
            content_type='application/json',
            status=400
        )
    user.password = new_password
    user.save()
    return HttpResponse(
        json.dumps({"message": _("Password changed successfully")}),
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
            json.dumps({"message": _("Code is required"), "type": "oauth_login_fail"}),
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
            json.dumps({"message": _("Invalid code"), "type": "oauth_login_fail"}),
            content_type='application/json',
            status=400
        )
    data = response.json()
    user = User.objects.get_or_create_42_user(data)
    return generate_login(request, user)


def send_verification_email(user: User):
    email_code = str(hashlib.sha256(os.urandom(1024)).hexdigest())
    cache.set(f'{user.id}_email_code', email_code, timeout=300)

    mail_client = MailClient()
    mail_client.send_mail(
        mail=user.email,
        subject=_("Email verification"),
        reply_to="noreply@neon-pong.com",
        message=f"<p>{_('Click on the following link to verify your email account')}: <a href='{settings.BASE_URL}/auth/verify_email?code={email_code}&user={user.id}'>{settings.BASE_URL}/auth/verify_email?code={email_code}&user={user.id}</a></p><p>{_('This link will expire in 5 minutes')}</p>",
        subtype="html"
    )


@require_http_methods(["POST"])
def send_verification_email_view(request: HttpRequest):
    data = request.json()
    if not data.get('user_id'):
        return HttpResponse(
            json.dumps({"message": _("User ID is required"), "type": "send_verification_email_fail"}),
            content_type='application/json',
            status=400
        )
    try:
        user: User = User.objects.get(pk=data.get('user_id'))
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": _("User not found"), "type": "send_verification_email_fail"}),
            content_type='application/json',
            status=400
        )
    send_verification_email(user)
    return HttpResponse(
        json.dumps({"message": _("Verification email sent")}),
        content_type='application/json',
        status=200
    )


@require_http_methods(["POST"])
def verify_email(request: HttpRequest):
    data = request.json()
    if not data.get('code'):
        return HttpResponse(
            json.dumps({"message": _("Code is required"), "type": "verify_email_fail"}),
            content_type='application/json',
            status=400
        )
    code = data.get('code')
    user_id = data.get('user')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse(
            json.dumps({"message": _("Invalid code"), "type": "verify_email_fail"}),
            content_type='application/json',
            status=400
        )
    sentinel = object()
    expected_code = cache.get(f'{user.id}_email_code', sentinel)
    if expected_code is sentinel or expected_code != code:
        return HttpResponse(
            json.dumps({"message": _("Code expired"), "type": "verify_email_fail"}),
            content_type='application/json',
            status=400
        )
    user.verified_email = True
    user.save()
    cache.delete(f'{user.id}_email_code')
    return HttpResponse(
        json.dumps({"message": _("Email verified")}),
        content_type='application/json',
        status=200
    )
