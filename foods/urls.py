from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, FoodViewSet

router = DefaultRouter()
router.register(r"foods", FoodViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = []

urlpatterns += router.urls
