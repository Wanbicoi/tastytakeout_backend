from rest_framework.routers import DefaultRouter

from .views import StoreViewSet, VerificationViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet)
router.register(r"stores", VerificationViewSet)

urlpatterns = []

urlpatterns += router.urls
