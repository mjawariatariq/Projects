import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from rtc_app.models import Room, Message, User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_name}'

        # Debug log for connection
        print(f"Connecting to WebSocket for room: {self.room_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.accept()

        # Debug log to confirm connection
        print(f"WebSocket connected to room: {self.room_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Debug log for disconnection
        print(f"Disconnected from room: {self.room_name}")

    async def receive(self, text_data):
        try:
            # Parse the incoming JSON data
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")
            username = text_data_json.get("username")
            room_name = text_data_json.get("room_name")

            # Debug log for received data
            print(f"Received message: {message} from {username} in room {room_name}")

            if not message or not username or not room_name:
                raise ValueError("Invalid WebSocket data.")

            # Save the message to the database
            await self.save_message(username, room_name, message)

            # Broadcast the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "room_name": room_name,
                }
            )

            # Debug log for message broadcast
            print(f"Message broadcasted to room {self.room_group_name}")

        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room_name = event["room_name"]

        # Debug log for received broadcast message
        print(f"Broadcasted message received: {message} from {username} in room {room_name}")

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "room_name": room_name,  # Include room name in the response
        }))

    @database_sync_to_async
    def save_message(self, username, room_name, message):
        try:
            user = User.objects.get(username=username)
            room = Room.objects.get(slug=room_name)  # Use slug to find the room
            Message.objects.create(user=user, room=room, content=message)
            print(f"Message saved: {message}")  # Debug log
        except User.DoesNotExist:
            print(f"User with username {username} does not exist.")
        except Room.DoesNotExist:
            print(f"Room with slug {room_name} does not exist.")
        except Exception as e:
            print(f"Error saving message: {e}")
