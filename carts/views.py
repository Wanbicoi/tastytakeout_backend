from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from carts.models import Cart
from carts.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):  # type: ignore
        return Cart.objects.filter(buyer=self.request.user)
