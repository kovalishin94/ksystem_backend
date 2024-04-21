import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
from django.urls import re_path

from chat.consumers import ChatConsumer
from security.middleware import JwtAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ksystem_backend.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(
                URLRouter(
                    [
                        re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
                    ]
                )
            )
        )
    }
)
