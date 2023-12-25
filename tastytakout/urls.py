# from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(title="Tasty Takout API", default_version="v1"),
    public=True,
)


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger")),
    path("", include("users.urls")),
    path("", include("stores.urls")),
    path("", include("chat.urls")),
    path("", include("foods.urls")),
    path("", include("carts.urls")),
    path("", include("orders.urls")),
]
