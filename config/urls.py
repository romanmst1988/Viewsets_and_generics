from django.contrib import admin

# маршрут для пустого URL
from django.http import HttpResponse
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDeleteAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)
from users.views import UserViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
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
    path("users/", include("users.urls", namespace="users")),
    path('materials/', include('materials.urls')),
    path('admin/', admin.site.urls),
    path('materials/', include('materials.urls')),
    path('users/', include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('', include('docs.urls')),
]