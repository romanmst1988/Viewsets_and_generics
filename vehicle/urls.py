from django.urls import path
from vehicle.apps import VehicleConfig
from rest_framework.routers import DefaultRouter

from vehicle.views import CarViewSet, MotoCreateAPIView, MotoListAPIView, MotoRetrieveAPIView, MotoUpdateAPIView, \
    MotoDestroyAPIView

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