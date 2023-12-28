from rest_framework import serializers
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "avatar_url",
            "name",
            "bio",
            "address",
            "date_of_birth",
            "gender",
        ]


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
