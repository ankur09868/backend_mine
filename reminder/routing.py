# routing.py

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumer import MyConsumer

urlpatterns = [
    path('ws/reminders/', MyConsumer.as_asgi()),
]

