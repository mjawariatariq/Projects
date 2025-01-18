# os module ko import kar rahe hain
import os
# Django ka asgi application import kar rahe hain
from django.core.asgi import get_asgi_application

# Django settings module ko set kar rahe hain
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetworkChatApplication.settings')

# Channels ke auth middleware aur routing import kar rahe hain
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
# Apni routing file ko import kar rahe hain
from . import routing

# ProtocolTypeRouter ka istemal karke application configure kar rahe hain
application = ProtocolTypeRouter(
    {
        # HTTP requests ko handle karne ke liye get_asgi_application ka istemal
        "http" : get_asgi_application() ,
        # WebSocket requests ko handle karne ke liye AuthMiddlewareStack aur URLRouter ka istemal
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )   
        )
    }
)
