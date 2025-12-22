from django.contrib import admin
# маршрут для пустого URL
from django.http import HttpResponse
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonListAPIView, LessonRetrieveAPIView)
from users.views import UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Courses API",
        default_version="v1",
        description="Документация для сервиса курсов и уроков",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


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
    path("users/", include("users.urls", namespace="users")),
    path("materials/", include("materials.urls")),
    path("materials/", include("materials.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path('', include('docs.urls')),
]
