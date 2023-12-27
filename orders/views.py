from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers import GetOrderSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):  # type: ignore
        return Order.objects.filter(buyer=self.request.user)
