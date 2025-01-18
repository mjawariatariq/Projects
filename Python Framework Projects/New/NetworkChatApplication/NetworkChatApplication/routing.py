# Django se URL patterns aur include, re_path ko import kar rahe hain
from django.urls import path, include, re_path
# Apni ChatConsumer ko import kar rahe hain
from .consumers import ChatConsumer

# WebSocket URLs ko define kar rahe hain
websocket_urlpatterns = [
    # Room slug ko path mein pass kar rahe hain aur ChatConsumer ko as_asgi() ke saath use kar rahe hain
    path("<room_slug>", ChatConsumer.as_asgi()),
    # Regular expression ke zariye room_slug ko capture kar rahe hain aur ChatConsumer ko as_asgi() ke saath use kar rahe hain
    re_path(r'^ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
]
