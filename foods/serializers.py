from rest_framework import serializers

from stores.serializers import StoreSerializer
from .models import Category, Food, FoodComment, FoodDiscount


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FoodCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodComment
        fields = ["content", "rating"]


class FoodDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDiscount
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    store = StoreSerializer()
    comments = FoodCommentSerializer(many=True)

    class Meta:
        model = Food
        fields = "__all__"
