from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from carts.models import Cart
from carts.serializers import CartSerializer, GetCartSerializer


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetCartSerializer
        else:
            return CartSerializer

    def get_queryset(self):  # type: ignore
        return Cart.objects.filter(buyer=self.request.user)
