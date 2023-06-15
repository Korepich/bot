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

    async def receive(self, text_data):
        message = json.loads(text_data)

        await self.channel_layer.group_send(
            "bot",
            {
                "type": "approve_door_action",
                "message": message["message"],
                "status": message["status"],
            },
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )


class BotNotificationConsumer(AsyncJsonWebsocketConsumer):
    room_group_name = "bot"

    async def send_action(self, event):
        msg = json.dumps({"message": event["message"], "method": "thief_confirmation"})

        await self.send(msg)

    async def receive(self, text_data):
        message = json.loads(text_data)

        await self.channel_layer.group_send(
            "mk",
            {
                "type": "send_action",
                "message": message["message"],
            },
        )

    async def approve_door_action(self, event):
        msg = json.dumps(
            {
                "message": event["message"],
                "method": "approve_door_action",
                "status": event["status"],
            }
        )

        await self.send(msg)

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )
