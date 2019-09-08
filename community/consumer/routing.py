from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/catchmind/<str:room_name>/', consumer.Consumer),
]
