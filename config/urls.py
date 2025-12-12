from django.contrib import admin
# маршрут для пустого URL
from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDeleteAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)
from users.views import UserViewSet


def home(request):
    return HttpResponse("<h1>API работает</h1><p>Используйте /api/</p>")


router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", home),  # пустой маршрут
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path(
        "api/lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"
    ),
    path("api/lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "api/lessons/<int:pk>/update/",
        LessonUpdateAPIView.as_view(),
        name="lesson_update",
    ),
    path(
        "api/lessons/<int:pk>/delete/",
        LessonDeleteAPIView.as_view(),
        name="lesson_delete",
    ),
    path("users/",include("users.urls", namespace="users")),
]
