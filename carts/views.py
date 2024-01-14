from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carts.models import Cart
from carts.serializers import CartSerializer, GetCartSerializer


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore
        return Cart.objects.select_related(
            "food", "food__category", "food__store"
        ).filter(buyer=self.request.user)

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetCartSerializer
        else:
            return CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        food_id = request.data.get("food")
        quantity = request.data.get("quantity")

        existing_cart = (
            Cart.objects.select_related("food")
            .filter(buyer=request.user, food__id=food_id)
            .first()
        )

        if existing_cart:
            existing_cart.quantity += quantity
            existing_cart.save()
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
