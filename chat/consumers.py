import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.role = str(self.scope["user"].role)
        user_id = str(self.scope["user"].id)
        tmp = self.room_name.split("_")
        buyer_id = tmp[0]
        # store_id = tmp[1]  # TODO: Check valid store
        print(user_id)
        if self.role == "BUYER" and user_id != buyer_id:
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # message = text_data

        # Save the message to the database

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "role": self.role},
        )

    @database_sync_to_async
    def create_chat(self, message, sender):
        tmp = self.room_name.split("_")
        buyer_id = tmp[0]
        store_id = tmp[1]
        Chat.objects.create(
            message=message,
            sender=sender if sender == "BUYER" else "STORE",
            buyer_id=buyer_id,
            store_id=store_id,
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["role"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
        await self.create_chat(message, self.role)
