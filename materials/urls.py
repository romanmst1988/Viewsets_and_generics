from django.urls import path
from materials.views import SubscriptionAPIView

urlpatterns = [
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
]
