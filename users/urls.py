from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProfileViewSet, account_registration, account_login

router = DefaultRouter()
router.register(r"users", ProfileViewSet)

urlpatterns = [
    path("users/login", account_login),
    path("users/register", account_registration),
]

urlpatterns += router.urls
