from rest_framework import serializers
from foods.serializers import FoodSerializer
from orders.serializers import VoucherSerializer


class GetHomeDataSerializer(serializers.Serializer):
    bannerUrls = serializers.JSONField()
    foods = FoodSerializer(many=True)
    vouchers = VoucherSerializer(many=True)


class HomeDataSerializer(serializers.Serializer):
    bannerUrls = serializers.JSONField()
    foodIds = serializers.JSONField()
    voucherIds = serializers.JSONField()
