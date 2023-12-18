# yourappname/serializers.py
from rest_framework import serializers
from .models import (
    User,
    Cart,
    Category,
    Food,
    FoodComment,
    Store,
    Order,
    OrderFood,
    BuyerLikeFood,
    BuyerLikeStore,
    Voucher,
    FoodDiscount,
    Chat,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class FoodCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodComment
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFood
        fields = "__all__"


class BuyerLikeFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerLikeFood
        fields = "__all__"


class BuyerLikeStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerLikeStore
        fields = "__all__"


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"


class FoodDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDiscount
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
