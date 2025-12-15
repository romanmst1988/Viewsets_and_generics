from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import SubscriptionAPIView, LessonViewSet, CourseViewSet

urlpatterns = [
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
]

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')


