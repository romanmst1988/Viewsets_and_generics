from rest_framework import serializers

from .models import CustomUser, Payment


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         exclude = ("password",)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, data):
        # валидация: либо course, либо lesson, либо одно из них
        if data.get("course") and data.get("lesson"):
            raise serializers.ValidationError(
                "Можно указать либо курс, либо урок, но не оба одновременно."
            )
        if not data.get("course") and not data.get("lesson"):
            raise serializers.ValidationError(
                "Должен быть указан либо курс, либо урок."
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "payments"]
