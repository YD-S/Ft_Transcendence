import datetime

import jwt
from django.core.cache import cache
from django.shortcuts import redirect

from NeonPong import settings
from common.request import HttpRequest

from users.models import User
from utils.exception import HttpError, UnauthorizedError


class TokenManager:
    __instance = None
    __initialized = False

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(TokenManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.refresh_token_history = {}
        self.sentinel = object()

    def create_token_pair(self, user_id, refresh_expiration=None):
        access_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        refresh_expiration = refresh_expiration or datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            hours=settings.REFRESH_TOKEN_EXPIRATION_HOURS)
        access_token = jwt.encode({'user_id': user_id, "exp": access_expiration}, settings.SECRET_KEY,
                                  algorithm='HS256')
        refresh_token = jwt.encode({'user_id': user_id, "exp": refresh_expiration}, settings.SECRET_KEY,
                                   algorithm='HS256')
        self.refresh_token_history[user_id] = self.refresh_token_history.get(user_id, [])[:-settings.REFRESH_TOKEN_HISTORY_SIZE]
        self.refresh_token_history[user_id].append(refresh_token)
        cache.set(f'user:{user_id}:token', access_token, timeout=settings.ACCESS_TOKEN_EXPIRATION_MINUTES * 60)
        return access_token, refresh_token, access_expiration, refresh_expiration

    def refresh_token(self, refresh_token):
        payload = self._test_token(refresh_token)
        exp = datetime.datetime.fromtimestamp(payload.get('exp'), datetime.UTC)
        if cache.get(f'user:{payload.get("user_id")}:token', self.sentinel) is self.sentinel:
            raise UnauthorizedError()
        return self.create_token_pair(payload.get('user_id'), exp)

    def validate_token(self, token):
        payload = self._test_token(token)

        if cache.get(f'user:{payload.get("user_id")}:token', self.sentinel) is self.sentinel:
            raise UnauthorizedError()
        if cache.get(f'user:{payload.get("user_id")}:token') != token:
            raise UnauthorizedError()
        return True

    def revoke_token(self, token):
        payload = self._test_token(token)
        if cache.get(f'user:{payload.get("user_id")}:token', self.sentinel) is not self.sentinel:
            cache.delete(f'user:{payload.get("user_id")}:token')
        else:
            raise UnauthorizedError()

    def _test_token(self, token, check_reuse=True):
        # Check for refresh token reuse
        if check_reuse:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            except jwt.DecodeError:
                raise UnauthorizedError()
            tokens = self.refresh_token_history.get(payload.get('user_id'), [])
            if token in tokens[:-1]:  # Check all but the last token, which is the current one
                self.revoke_token(tokens[-1])  # Revoke the current token
                raise UnauthorizedError()

        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError()
        except jwt.InvalidTokenError:
            raise UnauthorizedError()
        return payload


# Decorator to automatically check the token
def require_token(login_redirect=True):
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if settings.BYPASS_TOKEN:
                return func(request, *args, **kwargs)
            try:
                token = get_token(request)
                TokenManager().validate_token(token)
            except HttpError as e:
                if login_redirect and request.headers.get("Sec-Fetch-Mode") == "navigate":
                    return redirect("/auth/login")
                return e.as_http_response()
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": not settings.BYPASS_TOKEN})


def get_user(token: str):
    payload = decode_token(token)
    return User.objects.get(pk=payload.get('user_id'))


def get_token(request: HttpRequest):
    # Get token from Authorization cookie
    cookie = request.headers.get("Cookie")
    if not cookie:
        raise UnauthorizedError()
    token = None
    for c in cookie.split(";"):
        if c.strip().startswith("Authorization="):
            token = c.split("=")[1].strip()
            break
    if not token:
        raise UnauthorizedError()
    return token
