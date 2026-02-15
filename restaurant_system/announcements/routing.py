from django.urls import re_path
from .consumers import AnnouncementConsumer

websocket_urlpatterns = [
    re_path(r'ws/announcements/$', AnnouncementConsumer.as_asgi()),
]
