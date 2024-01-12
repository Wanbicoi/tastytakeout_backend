from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
    # local urls
    path("", include("users.urls")),
    path("", include("stores.urls")),
    path("", include("chat.urls")),
    path("", include("foods.urls")),
    path("", include("carts.urls")),
    path("", include("orders.urls")),
    path("", include("key_values.urls")),
]
