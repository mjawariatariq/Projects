import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from rtc_app.models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the room name from URL route kwargs
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse the received message
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        room_name = text_data_json.get("room_name")

        # Ensure we have the necessary data before proceeding
        if not message or not username or not room_name:
            return

        # Save the message in the database
        await self.save_message(message, username, room_name)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
            }
        )

    async def sendMessage(self, event):
        # Send the message to WebSocket
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

    @sync_to_async
    def save_message(self, message, username, room_name):
        print(f"Saving message: {username} in room: {room_name}...")

        try:
            # Fetch the user and room from the database
            user = User.objects.get(username=username)
            room = Room.objects.get(name=room_name)

            # Save the message
            Message.objects.create(user=user, room=room, content=message)
        except User.DoesNotExist:
            print(f"User {username} not found.")
        except Room.DoesNotExist:
            print(f"Room {room_name} not found.")
