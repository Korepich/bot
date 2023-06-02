from django.urls import re_path

from .consumer import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"api/v1/notifications/action", NotificationConsumer.as_asgi()),
]
