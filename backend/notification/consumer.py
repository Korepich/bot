import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class MkNotificationConsumer(AsyncJsonWebsocketConsumer):
    room_group_name = "mk"

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def send_action(self, event):
        msg = json.dumps(
            {
                "message": event["message"],
            }
        )

        await self.send(msg)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )


class BotNotificationConsumer(MkNotificationConsumer):
    room_group_name = "bot"
