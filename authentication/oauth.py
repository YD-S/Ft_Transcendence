import datetime
import hashlib
import os

import requests

from NeonPong import settings


# Decorator for methods that require an access token
def require_access_token(func):
    def wrapper(self, *args, **kwargs):
        if self.token_expiration < datetime.datetime.now():
            self.get_access_token()
        return func(self, *args, **kwargs)

    return wrapper


# Redirect user to 42 for authentication
# https://api.intra.42.fr/oauth/authorize?client_id=your_very_long_client_id&redirect_uri=http%3A%2F%2Flocalhost%3A1919%2Fusers%2Fauth%2Fft%2Fcallback&response_type=code&scope=public&state=a_very_long_random_string_witchmust_be_unguessable'

# Get access token
# curl -F grant_type=authorization_code \
# -F client_id=9b36d8c0db59eff5038aea7a417d73e69aea75b41aac771816d2ef1b3109cc2f \
# -F client_secret=d6ea27703957b69939b8104ed4524595e210cd2e79af587744a7eb6e58f5b3d2 \
# -F code=fd0847dbb559752d932dd3c1ac34ff98d27b11fe2fea5a864f44740cd7919ad0 \
# -F redirect_uri=https://myawesomeweb.site/callback \
# -X POST https://api.intra.42.fr/oauth/token

