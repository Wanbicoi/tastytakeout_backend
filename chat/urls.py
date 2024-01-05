from django.urls import path
from chat.views import list_chat, retrieve_chat

urlpatterns = [
    path("chat", list_chat),
    path("chat/<str:chat_room_id>/", retrieve_chat),
]
