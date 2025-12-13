from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, CustomUser
from .serializers import PaymentSerializer
from .filters import PaymentFilter

from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsOwnerProfile

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerProfile()]
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]