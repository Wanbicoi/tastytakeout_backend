from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import Chat
from chat.serializers import ChatSerializer


@api_view(["GET"])
@extend_schema(request=ChatSerializer)
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
        print("asd", store_id)
        latest_chats = (
            Chat.objects.filter(store=store_id)
            .order_by("store_id", "-created_at")
            .distinct("store_id")
        )

    serializer = ChatSerializer(latest_chats, many=True)
    return Response(serializer.data)
