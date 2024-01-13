from django.db.models import fields
from rest_framework import serializers

from users.models import User
from .models import Order, OrderFood, Voucher


class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFood
        exclude = ("order",)

    # def get_total(self, instance):
    #     return instance.quantity * instance.food.price


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = [
            "id",
            "code",
            "name",
            "description",
            "end",
            "created_at",
            "discount_amount",
            "discount_type",
            "max_price",
            "min_price",
        ]


class BuyerSerializer(serializers.ModelSerializer):
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
        ]


class GetOrderSerializer(serializers.ModelSerializer):
    foods = OrderFoodSerializer(many=True)
    buyer = BuyerSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    foods = OrderFoodSerializer(many=True)

    class Meta:
        model = Order
        exclude = ("buyer",)

    def create(self, validated_data):
        request = self.context.get("request")
        foods_data = validated_data.pop("foods", [])
        order = Order.objects.create(buyer=request.user, **validated_data)  # type: ignore

        for food_data in foods_data:
            OrderFood.objects.create(order=order, **food_data)
        return order
