from rest_framework import serializers
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
        fields = "__all__"


class GetOrderSerializer(serializers.ModelSerializer):
    foods = OrderFoodSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    # def get_total(self, instance):
    #     total = sum(food["quantity"] * food["food"]["price"] for food in instance.foods)
    #     return total


class OrderSerializer(serializers.ModelSerializer):
    foods = OrderFoodSerializer(many=True)

    class Meta:
        model = Order
        exclude = ("buyer", "store")

    def create(self, validated_data):
        request = self.context.get("request")
        newOrder = Order(buyer=request.user, **validated_data)  # type: ignore
        return newOrder
