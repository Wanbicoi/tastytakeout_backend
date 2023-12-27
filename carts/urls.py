from rest_framework.routers import DefaultRouter

from carts.views import CartViewSet


router = DefaultRouter()
router.register(r"carts", CartViewSet)
urlpatterns = []
urlpatterns += router.urls
