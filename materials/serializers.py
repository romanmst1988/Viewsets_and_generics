from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lessons_count']

    def get_lessons_count(self, obj):
        # используем related_name 'lessons' (определён в models.Lesson)
        return obj.lessons.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lessons', many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
