from django.urls import path

from key_values.views import home_data

urlpatterns = [path("home", home_data)]
