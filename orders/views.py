from rest_framework import viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F
from rest_framework.decorators import action, api_view

from drf_spectacular.utils import extend_schema
from rest_framework import status

from orders.serializers import (
    GetOrderSerializer,
    OrderSerializer,
    VoucherSerializer,
    YearSerializer,
)

from .schema import YearSchema
from django.db.models import Sum
from django.db.models.functions import TruncMonth


from orders.models import Event, Order, Voucher
from orders.serializers import (
    EventSerializer,
    GetEventSerializer,
)
from users.models import User
from utils.notify import notify


class EventViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.ViewSetMixin,
    GenericAPIView,
):
    queryset = Event.objects.prefetch_related("vouchers").all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):  # type: ignore
        if self.request.method == "GET":
            return GetEventSerializer
        else:
            return EventSerializer

    def perform_create(self, serializer):
        event = serializer.save()

        title = "Sự kiện ưu đãi 🤟"
        body = f"Ghé qua sự kiện: {event.name}"
        buyers = User.objects.filter(role="BUYER")
        for buyer in buyers:
            notify(title=title, body=body, userId=buyer.id)  # type:ignore


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
        if self.request.user.role == "BUYER":  # type:ignore
            return (
                Order.objects.select_related("buyer")
                .prefetch_related("foods")
                .filter(buyer=self.request.user)
            )
        store_id = self.request.auth.payload.get("store_id")  # type:ignore
        return (
            Order.objects.select_related("buyer")
            .prefetch_related("foods")
            .filter(foods__food__store=store_id)
            .distinct()
        )  # :> chả biết sao chạy đc nữa muôn đời ghét python

    def perform_update(self, serializer):
        order = serializer.save()
        notify(
            title="Đơn hàng đang được xử lý 🛳️",
            body="Mã đơn hàng #order_" + str(order.id),  # type:ignore
            userId=order.buyer.id,  # type:ignore
        )
        return order

    @action(detail=True, methods=["get"])
    def validate_voucher(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        voucher = order.voucher
        order_total = order.total

        if voucher.end < timezone.now():
            return Response({"valid": False, "message": "Voucher has expired"})

        if voucher.used_quantity >= voucher.quantity:
            return Response({"valid": False, "message": "Voucher has been fully used"})

        if order_total < voucher.min_price:
            return Response(
                {
                    "valid": False,
                    "message": "Order total does not meet voucher requirements",
                }
            )

        return Response({"valid": True, "message": "Voucher is valid for the order"})


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


class StatisticViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]  # admin
    schema = YearSchema()

    @extend_schema(request=YearSerializer)
    @action(detail=False, methods=["post"])
    def get_revenue(self, request):
        try:
            serializer = YearSerializer(data=request.data)
            if serializer.is_valid():
                year = serializer.data.get("year", False)

                orders = Order.objects.filter(created_at__year=year)
                count_orders = orders.count()

                complete_orders = orders.filter(status="COMPLETED")

                revenue_data = (
                    complete_orders.annotate(month=TruncMonth("created_at"))
                    .values("month")
                    .annotate(total_revenue_month=Sum("total"))
                    .order_by("month")
                )

                revenue = (
                    complete_orders.aggregate(total_revenue=Sum("total"))[
                        "total_revenue"
                    ]
                    or 0
                )

                count_complete_orders = complete_orders.count()

                response_data = {
                    "result": "Success",
                    "revenue_month": list(revenue_data),
                    "total_revenue": revenue,
                    "count_orders": count_orders,
                    "count_complete_orders": count_complete_orders,
                }

                return Response(response_data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)})
