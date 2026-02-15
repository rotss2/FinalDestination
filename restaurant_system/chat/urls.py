from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('thread/<int:thread_id>/', views.thread_view, name='thread'),
    path('support/', views.support_inbox, name='support_inbox'),
]
