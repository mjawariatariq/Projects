# JSON module ko import kar rahe hain
import json
# Channels ke WebsocketConsumer ko import kar rahe hain
from channels.generic.websocket import AsyncWebsocketConsumer
# asgiref ka sync_to_async function import kar rahe hain
from asgiref.sync import sync_to_async

# rtc_app ka models import kar rahe hain
from rtc_app.models import Room, Message, User

# ChatConsumer class define kar rahe hain jo WebSocket connections ko handle karegi
class ChatConsumer(AsyncWebsocketConsumer):
    # Connect hone par ye function call hoga
    async def connect(self):
        # Room ka naam URL se nikaal rahe hain
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        # Room group ka naam set kar rahe hain
        self.roomGroupName = 'chat_%s' % self.room_name
        
        # Channel layer ke group mein current channel ko add kar rahe hain
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        # WebSocket ko accept kar rahe hain
        await self.accept()
        
    # Disconnect hone par ye function call hoga
    async def disconnect(self, close_code):
        # Channel ko group se remove kar rahe hain
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    # Receive hone par ye function call hoga
    async def receive(self, text_data):
        # Received text data ko JSON mein convert kar rahe hain
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_name = text_data_json["room_name"]
        
        # Message ko database mein save kar rahe hain
        await self.save_message(message, username, room_name)

        # Message ko group ke saare clients ko bhej rahe hain
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
            }
        )
        
    # Ye function message ko client ko bhejega
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        # Message aur username ko WebSocket ke through send kar rahe hain
        await self.send(text_data=json.dumps({"message": message, "username": username}))
    
    # Sync function jo message ko database mein save karega
    @sync_to_async
    def save_message(self, message, username, room_name):
        print(username, room_name, "----------------------")
        # User aur room ko database se get kar rahe hain
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        
        # Message ko save kar rahe hain
        Message.objects.create(user=user, room=room, content=message)
