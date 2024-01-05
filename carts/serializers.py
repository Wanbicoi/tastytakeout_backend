from rest_framework import serializers
from itertools import groupby

from foods.models import Food
from foods.serializers import CategorySerializer
from stores.serializers import StoreSerializer
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("quantity", "food")

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user  # type: ignore
        cart = Cart(buyer=user, **validated_data)
        cart.save()
        return cart


class FoodCartSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    store = StoreSerializer()

    class Meta:
        model = Food
        fields = "__all__"


class GetCartSerializer(serializers.ModelSerializer):
    food = FoodCartSerializer()

    class Meta:
        model = Cart
        fields = ("quantity", "food")
