from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from utils.permissions import IsOwner
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import status
from django.http import JsonResponse

from carts.models import Cart
from orders.models import Order, Voucher, OrderFood
from orders.serializers import GetOrderSerializer, OrderSerializer, VoucherSerializer
from carts.serializers import GetCartSerializer

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


    @action(detail=True, methods=["get"])
    def validate_voucher(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        voucher=order.voucher
        order_total=order.total

        if voucher.end < timezone.now():
            return Response({'valid': False, 'message': 'Voucher has expired'})
        
        if voucher.used_quantity >= voucher.quantity:
            return Response({'valid': False, 'message': 'Voucher has been fully used'})
        
        if order_total < voucher.min_price:
            return Response({'valid': False, 'message': 'Order total does not meet voucher requirements'})

        return Response({'valid': True, 'message': 'Voucher is valid for the order'})


    @extend_schema(request=None)
    @action(detail=True, methods=["patch"])
    def deny(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.status = "DENIED"
        order.save()
        return Response({'message': 'Order denied'}, status=status.HTTP_200_OK)
    

    @extend_schema(request=None)
    @action(detail=True, methods=["patch"])
    def approve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.status = "APPROVED"
        order.save()
        return Response({'message': 'Order approved'}, status=status.HTTP_200_OK)


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
