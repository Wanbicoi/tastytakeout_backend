from rest_framework.routers import DefaultRouter

from .views import StoreViewSet, VerificationViewSet, StatisticViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet)
router.register(r"stores", VerificationViewSet)
router.register(r"stores", StatisticViewSet)

urlpatterns = []

urlpatterns += router.urls
