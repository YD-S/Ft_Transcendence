import datetime
import json

import jwt

from Api import settings
from common.request import HttpRequest

from users.models import User
from utils.exception import ValidationError


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

    def create_token_pair(self, user_id):
        access_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        refresh_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_DAYS)
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
        if payload.get('user_id') not in self.tokens:
            raise ValidationError(json.dumps({"message": "Invalid token", "type": "invalid_token"}),
                                  content_type='application/json')
        return self.create_token_pair(payload.get('user_id'))

    def validate_token(self, token):
        payload = self._test_token(token)
        if payload.get('user_id') not in self.tokens:
            raise ValidationError(json.dumps({"message": "Invalid token1", "type": "invalid_token"}),
                                  content_type='application/json')
        if self.tokens.get(payload.get('user_id')).get('access_token') != token:
            raise ValidationError(json.dumps({"message": "Invalid token2", "type": "invalid_token"}),
                                  content_type='application/json')
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
def require_token(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if settings.BYPASS_TOKEN:
            try:
                request.user = get_user(get_token(request))
            except ValidationError:
                request.user = None
            return func(request, *args, **kwargs)
        try:
            token = get_token(request)
            TokenManager().validate_token(token)
        except ValidationError as e:
            resp = e.as_http_response()
            resp.status_code = 401
            return resp
        request.user = get_user(token)
        return func(request, *args, **kwargs)

    return wrapper


def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": not settings.BYPASS_TOKEN})


def get_user(token: str):
    payload = decode_token(token)
    return User.objects.get(pk=payload.get('user_id'))


def get_token(request: HttpRequest):
    bearer_token = request.headers.get('Authorization')
    if not bearer_token:
        raise ValidationError(json.dumps({"message": "Token is required", "type": "token_required"}),
                              content_type='application/json')
    if not bearer_token.startswith("Bearer "):
        raise ValidationError(json.dumps({"message": "Expected Bearer token", "type": "invalid_token"}),
                              content_type='application/json')
    return bearer_token.split(" ")[1]
