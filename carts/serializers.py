from rest_framework import serializers
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
