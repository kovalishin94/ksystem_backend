import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
from django.urls import re_path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ksystem_backend.settings')
django_asgi_app = get_asgi_application()

from chat.consumers import ChatConsumer
from security.middleware import JwtAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(
                URLRouter(
                    [
                        re_path(
                            r"ws/chat/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
                    ]
                )
            )
        )
    }
)
