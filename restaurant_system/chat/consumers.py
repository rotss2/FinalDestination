import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatThread, ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = int(self.scope['url_route']['kwargs']['thread_id'])
        self.room_group_name = f'chat_thread_{self.thread_id}'

        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        allowed = await self._is_allowed(user.id, self.thread_id)
        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = (data.get("message") or "").strip()
        if not msg:
            return
        user = self.scope["user"]
        message = await self._save_message(self.thread_id, user.id, msg)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': {
                    "sender": user.username,
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def _save_message(self, thread_id, user_id, content):
        thread = ChatThread.objects.get(id=thread_id)
        user = User.objects.get(id=user_id)
        return ChatMessage.objects.create(thread=thread, sender=user, content=content)

    @database_sync_to_async
    def _is_allowed(self, user_id, thread_id):
        thread = ChatThread.objects.get(id=thread_id)
        user = User.objects.get(id=user_id)
        return (thread.customer_id == user_id) or user.is_staff or getattr(user, "is_support", False)
