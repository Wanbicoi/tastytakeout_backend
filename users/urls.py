from django.urls import path
from .views import (
    ChangePasswordView,
    UpdateProfileView,
    account_registration,
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", UpdateProfileView.as_view()),
    path("users/register", account_registration),
    path("users/password", ChangePasswordView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
]
