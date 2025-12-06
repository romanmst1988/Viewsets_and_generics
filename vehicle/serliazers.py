from rest_framework import serializers

from vehicle.models import Car, Moto


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = "__all__"
