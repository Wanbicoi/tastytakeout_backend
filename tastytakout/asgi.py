"""
ASGI config for tastytakout project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing
from channels_auth_token_middlewares.middleware import (
    QueryStringSimpleJWTAuthTokenMiddleware,
)

django_asgi_app = get_asgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tastytakout.settings")

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": QueryStringSimpleJWTAuthTokenMiddleware(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
