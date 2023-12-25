from rest_framework import serializers
from .models import Order, OrderFood, Voucher


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFood
        fields = "__all__"


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
