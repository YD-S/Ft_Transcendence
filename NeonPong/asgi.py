"""
ASGI config for Api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application

import routing.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NeonPong.settings")

MIDDLEWARE = [
    SessionMiddlewareStack,
    AuthMiddlewareStack
]

router = URLRouter(routing.routing.websocket_urlpatterns)
for middleware in MIDDLEWARE:
    router = middleware(router)
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(router),
})
