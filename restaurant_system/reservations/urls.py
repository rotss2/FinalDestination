from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('portal/', views.portal, name='portal'),
    path('new/', views.create_reservation, name='create_reservation'),
    path('edit/<int:res_id>/', views.edit_reservation, name='edit_reservation'),
    path('cancel/<int:res_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('check/', views.check_availability, name='check_availability'),

    path('queue/', views.queue_board, name='queue_board'),
    path('queue/add/', views.add_walkin, name='add_walkin'),
]
