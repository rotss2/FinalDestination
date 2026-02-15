import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from reservations.models import Announcement

class AnnouncementConsumer(AsyncWebsocketConsumer):
    group_name = "announcements"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def announcement_event(self, event):
        await self.send(text_data=json.dumps(event["data"]))

# Helper broadcaster (called from signals)
async def broadcast_announcement(channel_layer, announcement):
    await channel_layer.group_send(
        "announcements",
        {
            "type": "announcement.event",
            "data": {
                "title": announcement.title,
                "message": announcement.message,
                "priority": announcement.priority,
                "created_at": announcement.created_at.isoformat(),
            },
        },
    )
