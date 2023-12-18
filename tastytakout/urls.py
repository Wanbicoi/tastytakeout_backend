from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CartViewSet,
    CategoryViewSet,
    FoodViewSet,
    FoodCommentViewSet,
    StoreViewSet,
    OrderViewSet,
    OrderFoodViewSet,
    BuyerLikeFoodViewSet,
    BuyerLikeStoreViewSet,
    VoucherViewSet,
    FoodDiscountViewSet,
    ChatViewSet,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(title="Tasty Takout API", default_version="v1"),
    public=True,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"carts", CartViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"foods", FoodViewSet)
router.register(r"foodcomments", FoodCommentViewSet)
router.register(r"stores", StoreViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"orderfoods", OrderFoodViewSet)
router.register(r"buyerlikefoods", BuyerLikeFoodViewSet)
router.register(r"buyerlikestores", BuyerLikeStoreViewSet)
router.register(r"vouchers", VoucherViewSet)
router.register(r"fooddiscounts", FoodDiscountViewSet)
router.register(r"chats", ChatViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger")),
]

urlpatterns += router.urls
