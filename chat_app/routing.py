# Similar to urls.py for HTTP protocol

from django.urls import re_path, path

from . import consumers


websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/basic/<str:room_name>/', consumers.BasicChatConsumer.as_asgi()),

]

