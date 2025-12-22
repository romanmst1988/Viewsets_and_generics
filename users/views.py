import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import PaymentFilter
from .models import CustomUser, Payment
from .permissions import IsOwnerProfile
from .serializers import (PaymentSerializer, UserCreateSerializer,
                          UserSerializer)
from .services import (create_checkout_session, create_stripe_price,
                       create_stripe_product)

"""View для оплаты"""


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product = create_stripe_product(payment.course)
        price = create_stripe_price(product.id, payment.amount)
        session = create_checkout_session(price.id)

        payment.payment_url = session.url
        payment.stripe_session_id = session.id
        payment.save()


def retrieve_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwnerProfile()]
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]
