from django.urls import re_path

from .consumer import MkNotificationConsumer, BotNotificationConsumer

websocket_urlpatterns = [
    re_path(r"api/v1/notifications/action", MkNotificationConsumer.as_asgi()),
    re_path(r"api/v1/notifications/breaking", BotNotificationConsumer.as_asgi()),
]
