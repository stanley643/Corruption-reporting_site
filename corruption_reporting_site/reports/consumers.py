from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            # Handle text data
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message
            }))
        elif bytes_data:
            # Handle binary data (files, images, etc.)
            # You will need to save the file and send a message back with the file URL or identifier
            pass
# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast message to everyone connected to this WebSocket
        await self.channel_layer.group_send(
            'chat_group',
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
