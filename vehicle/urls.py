from django.urls import path
from rest_framework.routers import DefaultRouter

from vehicle.apps import VehicleConfig
from vehicle.views import (CarViewSet, MotoCreateAPIView, MotoDestroyAPIView,
                           MotoListAPIView, MotoRetrieveAPIView,
                           MotoUpdateAPIView)

app_name = VehicleConfig.name


router = DefaultRouter()
router.register(r"cars", CarViewSet)

urlpatterns = [
    path("moto/create/", MotoCreateAPIView.as_view(), name="moto_create"),
    path("moto/", MotoListAPIView.as_view(), name="moto_list"),
    path("moto/<int:pk>/", MotoRetrieveAPIView.as_view(), name="moto-get"),
    path("moto/update/<int:pk>/", MotoUpdateAPIView.as_view(), name="moto-update"),
    path("moto/delet/<int:pk>/", MotoDestroyAPIView.as_view(), name="moto-delete"),
] + router.urls
