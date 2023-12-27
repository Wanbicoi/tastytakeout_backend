from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import VoucherViewSet
from .views import count_valid_vouchers

router = DefaultRouter()
router.register(r"vouchers", VoucherViewSet)

urlpatterns = [
    path('vouchers/count-valid-vouchers/', count_valid_vouchers, name='count_valid_vouchers'),
]

urlpatterns += router.urls