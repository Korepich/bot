import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "1"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def send_action(self, event):
        msg = json.dumps(
            {
                "message": event["message"],
                "room_name": self.room_group_name,
                "channel_name": self.channel_name,
            }
        )

        await self.send(msg)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )
