from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F
from rest_framework.decorators import api_view

from orders.models import Order, Voucher
from orders.serializers import GetOrderSerializer, OrderSerializer, VoucherSerializer


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


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

    # For buyer: Get list of valid vouchers, sort by end date (ASC)
    def get_queryset(self):
        only_valid = self.request.query_params.get("only_valid", None)
        current_datetime = timezone.now()

        if only_valid == "true":
            return (
                Voucher.objects.all()
                .filter(end__gte=current_datetime, used_quantity__lt=F("quantity"))
                .order_by("end")
            )

    # For admin: Get list of all vouchers, sort by end date (DESC)
    def list(self, request):
        vouchers = self.queryset.order_by("-end")
        serializer = self.serializer_class(vouchers, many=True)
        return Response(serializer.data)


# Get the total number of valid vouchers
@api_view(["GET"])
def count_valid_vouchers(request):
    current_datetime = timezone.now()
    valid_vouchers_count = Voucher.objects.filter(
        end__gte=current_datetime, used_quantity__lt=F("quantity")
    ).count()

    return Response({"valid_vouchers_count": valid_vouchers_count}, status=200)
