from django.contrib import admin
from django.urls import path, include

from vehicle.views import CarViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("vehicle.urls", namespace="vehicle")),
]
