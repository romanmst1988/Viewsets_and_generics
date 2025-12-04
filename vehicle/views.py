from rest_framework import viewsets

from vehicle.models import Car
from vehicle.serliazers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()