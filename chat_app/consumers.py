import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Message, Room, Participant

@database_sync_to_async
def add_message_to_message(message, room, sender_type, sender):
    
    new_message = Message.objects.create(
            room=Room.objects.get(id=int(room)),
            sender=User.objects.get(id=int(sender)),
            sender_type=sender_type,
            message=message
        )
    print("ADDED TO DB")
    

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("CONNECT CALLED")
        print(self.channel_name)
        # print(self.scope['user'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("Valid user- ", self.scope['user'])
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        print("RECEIVE CALLED")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'room_id': text_data_json['room_id'],
                'sender': text_data_json['sender'],
                'sender_type': text_data_json['sender_type']
            }
        )

        # Add message to DB
        await add_message_to_message(message, text_data_json['room_id'], text_data_json['sender_type'], text_data_json['sender'])

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print("SEND CALLED")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'room_id': event['room_id'],
            'sender': event['sender'],
            'sender_type': event['sender_type']
        }))

      