from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProfileViewSet, account_registration, account_login
from .views import get_favorite_foods

router = DefaultRouter()
router.register(r"users", ProfileViewSet)

urlpatterns = [
    path("users/login", account_login),
    path("users/register", account_registration),
    path('users/<int:user_id>/favorite-foods/', get_favorite_foods, name='get-favorite-foods'),
]

urlpatterns += router.urls
