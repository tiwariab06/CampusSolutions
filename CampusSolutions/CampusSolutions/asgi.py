import os
from django.core.asgi import get_asgi_application

# FIRST set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CampusSolutions.settings")

# THEN import Django models AFTER setup
django_asgi_app = get_asgi_application()

# FINALLY import WebSocket routes
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import MainChat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(MainChat.routing.websocket_urlpatterns)
        ),
    }
)
