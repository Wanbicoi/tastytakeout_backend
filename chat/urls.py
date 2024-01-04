from django.urls import path
from chat.views import list_chat

urlpatterns = [
    path("chat", list_chat),
]
