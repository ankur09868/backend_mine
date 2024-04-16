# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import asyncio

class ReminderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        print("hehe")
        await self.channel_layer.group_add("reminder_group", self.channel_name)
        print("Connected to group 'reminder_group'")

    async def disconnect(self, close_code):
        pass  # No need to do anything when the WebSocket connection is closed

    async def receive(self, text_data):
        pass  # No need to handle incoming messages from clients in this case

    async def send_reminder_message(self, event):
        # Introduce a delay here (e.g., 5 seconds)
        await asyncio.sleep(5)

        # Send reminder message to the client
        reminder_data = event['message']
        delay=event['time']
        await asyncio.sleep(delay)
        await self.send(text_data=json.dumps({
            'reminder_message': reminder_data
        }))
        print("doneoneoneoneoneoneone")

