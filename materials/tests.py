from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import CustomUser


class LessonCRUDTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="user@test.com", password="12345"
        )

        self.course = Course.objects.create(
            title="Python", description="Test", owner=self.user  # 🔥 ВАЖНО
        )

        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            course=self.course,
            video_url="https://youtube.com/watch?v=123",
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            "title": "Lesson 2",
            "course": self.course.id,
            "video_link": "https://youtube.com/watch?v=456",
        }
        response = self.client.post("/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_video_link(self):
        data = {
            "title": "Lesson bad",
            "course": self.course.id,
            "video_url": "https://google.com/video",
        }
        response = self.client.post("/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="sub@test.com", password="12345"
        )

        self.course = Course.objects.create(
            title="Django", description="Framework", owner=self.user  # 🔥 ВАЖНО
        )

        self.client.force_authenticate(user=self.user)

    def test_subscribe_and_unsubscribe(self):
        url = "/materials/subscribe/"

        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.data["message"], "Подписка удалена")
