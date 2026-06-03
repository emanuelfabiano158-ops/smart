from django.urls import re_path
from .consumers import WaterConsumer

websocket_urlpatterns = [
    re_path(r'ws/water/$', WaterConsumer.as_asgi()),
]