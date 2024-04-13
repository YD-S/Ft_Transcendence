import datetime
import json
import logging

import jwt
from django.shortcuts import redirect

from NeonPong import settings
from common.request import HttpRequest

from users.models import User
from utils.exception import ValidationError, HttpError, UnauthorizedError


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
        self.tokens = {}

    def create_token_pair(self, user_id, refresh_expiration=None):
        access_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        refresh_expiration = refresh_expiration or datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_DAYS)
        access_token = jwt.encode({'user_id': user_id, "exp": access_expiration}, settings.SECRET_KEY,
                                  algorithm='HS256')
        refresh_token = jwt.encode({'user_id': user_id, "exp": refresh_expiration}, settings.SECRET_KEY,
                                   algorithm='HS256')
        self.tokens[user_id] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_expiration": f"{access_expiration:%Y-%m-%d %H:%M:%S}",
            "refresh_expiration": f"{refresh_expiration:%Y-%m-%d %H:%M:%S}"
        }
        return access_token, refresh_token, access_expiration, refresh_expiration

    def refresh_token(self, refresh_token):
        payload = self._test_token(refresh_token)
        exp = datetime.datetime.fromtimestamp(payload.get('exp'), datetime.UTC)
        if payload.get('user_id') not in self.tokens:
            raise UnauthorizedError()
        return self.create_token_pair(payload.get('user_id'), exp)

    def validate_token(self, token):
        payload = self._test_token(token)
        if payload.get('user_id') not in self.tokens:
            raise UnauthorizedError()
        if self.tokens.get(payload.get('user_id')).get('access_token') != token:
            raise UnauthorizedError()
        return True

    def revoke_token(self, token):
        payload = self._test_token(token)
        if payload.get('user_id') in self.tokens:
            del self.tokens[payload.get('user_id')]
        else:
            raise ValidationError(json.dumps({"message": "Invalid token", "type": "invalid_token"}),
                                  content_type='application/json')

    @staticmethod
    def _test_token(token):
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise ValidationError(json.dumps({"message": "Token expired", "type": "token_expired"}),
                                  content_type='application/json')
        except jwt.InvalidTokenError:
            raise ValidationError(json.dumps({"message": "Invalid token3", "type": "invalid_token"}),
                                  content_type='application/json')
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
                    return redirect("/login")
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
