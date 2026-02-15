from django.urls import path
from . import views

app_name = 'menu'
urlpatterns = [
    path('', views.menu_home, name='menu_home'),
    path('c/<slug:slug>/', views.category_detail, name='category_detail'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]
