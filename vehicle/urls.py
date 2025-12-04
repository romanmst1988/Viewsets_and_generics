from django.urls import path
from vehicle.apps import VehicleConfig
from rest_framework.routers import DefaultRouter

from vehicle.views import CarViewSet, MotoCreateAPIView

app_name = VehicleConfig.name


router = DefaultRouter()
router.register(r"cars", CarViewSet)

urlpatterns = [
    path("moto/create", MotoCreateAPIView.as_view(), name="moto_create"),
] + router.urls