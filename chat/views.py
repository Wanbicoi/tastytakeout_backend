from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat
from chat.serializers import ChatSerializer, GetChatSerializer, OpenApiChatSerializer
import re


@api_view(["GET"])
@extend_schema(request=GetChatSerializer)
@permission_classes([IsAuthenticated])
def list_chat(request):
    role = request.user.role
    if role == "BUYER":
        latest_chats = (
            Chat.objects.filter(buyer=request.user)
            .order_by("store_id", "-created_at")
            .distinct("store_id")
        )
    else:
        store_id = request.auth.payload.get("store_id")
        latest_chats = (
            Chat.objects.filter(store=store_id)
            .order_by("store_id", "-created_at")
            .distinct("store_id")
        )

    serializer = GetChatSerializer(latest_chats, many=True)
    return Response(serializer.data)


@extend_schema(request=OpenApiChatSerializer, responses=GetChatSerializer)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def retrieve_chat(request, chat_room_id):
    # TODO recheck
    pattern = r"^\d+_\d+"
    if not bool(re.match(pattern, chat_room_id)):
        return Response("Invalid chat room id", status=status.HTTP_400_BAD_REQUEST)

    tmp = chat_room_id.split("_")
    buyer_id = tmp[0]
    store_id = tmp[1]
    role = request.user.role
    if request.method == "GET":
        if role == "BUYER":
            chats = Chat.objects.filter(buyer=request.user, store=store_id)
        else:
            store_id = request.auth.payload.get("store_id")
            chats = Chat.objects.filter(store=store_id, buyer=buyer_id)

        serializer = GetChatSerializer(chats, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        if role == "BUYER":
            serializer = ChatSerializer(
                data={
                    "message": request.data.get("message"),
                    "sender": "BUYER",
                    "store": store_id,
                    "buyer": request.user.id,
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            store_id = request.auth.payload.get("store_id")
            serializer = ChatSerializer(
                data={
                    "message": request.data.get("message"),
                    "sender": "STORE",
                    "store": store_id,
                    "buyer": buyer_id,
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response()
