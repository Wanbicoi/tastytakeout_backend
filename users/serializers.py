from rest_framework import serializers
from stores.models import Store

from stores.serializers import FoodSerializer
from .models import User


class ProfileStoreSerializer(serializers.ModelSerializer):
    likers_count = serializers.SerializerMethodField()
    foods = FoodSerializer(many=True)

    def get_likers_count(self, obj):
        return obj.likers.count()

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "image_url",
            "address",
            "likers_count",
            "foods",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    stores = ProfileStoreSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "avatar_url",
            "name",
            "bio",
            "address",
            "date_of_birth",
            "gender",
            "stores",
        ]

    def __init__(self, *args, **kwargs):
        # Call the parent __init__ method
        super(ProfileSerializer, self).__init__(*args, **kwargs)

        if self.context.get("request") and self.context["request"].method in [
            "PATCH",
            "PUT",
        ]:
            self.fields.pop("username", None)


class RegisterUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password", "role")
        extra_kwargs = {"password": {"write_only": True}}


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    fcm_token = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class FCMTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
