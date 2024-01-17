from django.db.models import fields
from django.shortcuts import get_list_or_404
from rest_framework import serializers

from users.models import User
from .models import Event, Order, OrderFood, Voucher

from .models import Order, OrderFood, Voucher
from foods.serializers import FoodSerializer

class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFood
        exclude = ("order",)

    # def get_total(self, instance):
    #     return instance.quantity * instance.food.price


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        exclude = ("event",)


class GetEventSerializer(serializers.ModelSerializer):
    vouchers = VoucherSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


class PostVoucherSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class EventSerializer(serializers.ModelSerializer):
    vouchers = PostVoucherSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        vouchers_data = validated_data.pop("vouchers", [])

        event = Event.objects.create(**validated_data)
        if len(vouchers_data) > 0:
            vouchers = get_list_or_404(
                Voucher, pk__in=[voucher["id"] for voucher in vouchers_data]
            )  # WARN Đừng bao giờ dùng Language ko có type-safe như python, javascript nhé :))) sucks
            event.vouchers.add(*vouchers)
        return event


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


class YearSerializer(serializers.Serializer):
    year = serializers.IntegerField()
