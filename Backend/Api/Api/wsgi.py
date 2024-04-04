"""
WSGI config for Api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.wsgi import get_wsgi_application

import routing.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Api.settings")

application = ProtocolTypeRouter({
    "http": get_wsgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.routing.websocket_urlpatterns
            )
        )
    ),
})
