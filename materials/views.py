from django.contrib.auth.base_user import BaseUserManager
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.paginators import CourseLessonPagination
from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer

from django.utils import timezone
from materials.tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), ~IsModerator()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Создание курса",
        request_body=CourseSerializer,
        responses={201: CourseSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновление курса",
        request_body=CourseSerializer,
        responses={200: CourseSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление курса",
        request_body=CourseSerializer,
        responses={200: CourseSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление курса", responses={204: "Курс удалён"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Вызов задачи в контроллере обновления курса
    def perform_update(self, serializer):
        course = serializer.save()

        if not course.can_send_notification():
            return

        subscriptions = Subscription.objects.filter(course=course)
        emails = [sub.user.email for sub in subscriptions if sub.user.email]

        if emails:
            send_course_update_email.delay(emails, course.title)


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination

    @swagger_auto_schema(
        operation_description="Создание урока",
        request_body=LessonSerializer,
        responses={201: LessonSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    @swagger_auto_schema(
        operation_description="Создание урока (Generic)",
        request_body=LessonSerializer,
        responses={201: LessonSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    @swagger_auto_schema(
        operation_description="Получение урока", responses={200: LessonSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновление урока",
        request_body=LessonSerializer,
        responses={200: LessonSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление урока", responses={204: "Урок удалён"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Список уроков",
        responses={200: LessonSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @swagger_auto_schema(
        operation_description="Получение урока", responses={200: LessonSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Подписка / отписка от курса",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID курса"
                )
            },
            required=["course_id"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
            )
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
