import os

from channels.auth import AuthMiddlewareStack
from .custom_user_middleware import CustomAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": CustomAuthMiddleware(
        URLRouter(
            # To use routes that we created
            websocket_urlpatterns
        )
    ),
    
})