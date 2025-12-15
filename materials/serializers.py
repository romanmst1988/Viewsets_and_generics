from rest_framework import serializers
from .models import Course, Lesson
from materials.validators import youtube_only_validator
from materials.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            youtube_only_validator
        ]


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()

    def get_lessons_count(self, obj):
        # используем related_name 'lessons' (определён в models.Lesson)
        return obj.lessons.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lessons", many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
