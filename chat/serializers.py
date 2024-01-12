from rest_framework import serializers
from stores.models import Store
from users.models import User
from .models import Chat


class ChatStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "image_url"]


class ChatProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar_url", "name"]


class OpenApiChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("message",)


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("buyer", "store", "message", "sender")


class GetChatSerializer(serializers.ModelSerializer):
    chat_room_id = serializers.SerializerMethodField()
    store = ChatStoreSerializer()
    buyer = ChatProfileSerializer()

    def get_chat_room_id(self, obj):
        buyer_id_str = str(obj.buyer.id)
        store_id_str = str(obj.store.id)
        return buyer_id_str + "_" + store_id_str

    class Meta:
        model = Chat
        fields = "__all__"
