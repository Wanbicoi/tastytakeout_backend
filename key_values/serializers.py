from rest_framework import serializers
from foods.models import Food
from orders.models import Voucher


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "description"]  # Include only the necessary fields


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ["id", "name", "discount"]  # Include only the necessary fields


class GetHomeDataSerializer(serializers.Serializer):
    bannerUrls = serializers.JSONField()
    foods = FoodSerializer(many=True)
    vouchers = VoucherSerializer(many=True)


class HomeDataSerializer(serializers.Serializer):
    bannerUrls = serializers.JSONField()
    foodIds = serializers.JSONField()
    voucherIds = serializers.JSONField()
