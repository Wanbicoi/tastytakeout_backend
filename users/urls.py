from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProfileViewSet, account_registration
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r"users", ProfileViewSet)

urlpatterns = [
    # path("users/login", account_login),
    path("users/register", account_registration),
    path("users/login/", TokenObtainPairView.as_view()),
]

urlpatterns += router.urls
