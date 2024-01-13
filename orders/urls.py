from rest_framework.routers import DefaultRouter
from django.urls import path

from orders.views import OrderViewSet, VoucherViewSet, count_valid_vouchers, StatisticViewSet


router = DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"vouchers", VoucherViewSet)
router.register(r"statistic", StatisticViewSet)
urlpatterns = [
    path(
        "vouchers/count-valid-vouchers/",
        count_valid_vouchers,
        name="count_valid_vouchers",
    ),
]
urlpatterns += router.urls
