from django.urls import path
from . import views

app_name = 'announcements'
urlpatterns = [
    path('', views.live_board, name='live_board'),
]
