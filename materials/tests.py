from django.test import TestCase

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from users.models import CustomUser
from materials.models import Course, Lesson, Subscription


class LessonCRUDTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@test.com',
            password='12345'
        )
        self.course = Course.objects.create(
            title='Python',
            description='Test'
        )
        self.lesson = Lesson.objects.create(
            title='Lesson 1',
            course=self.course,
            video_link='https://youtube.com/watch?v=123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'title': 'Lesson 2',
            'course': self.course.id,
            'video_link': 'https://youtube.com/watch?v=456'
        }
        response = self.client.post('/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_video_link(self):
        data = {
            'title': 'Lesson bad',
            'course': self.course.id,
            'video_link': 'https://google.com/video'
        }
        response = self.client.post('/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='sub@test.com',
            password='12345'
        )
        self.course = Course.objects.create(
            title='Django',
            description='Framework'
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_and_unsubscribe(self):
        url = reverse('subscribe')

        response = self.client.post(url, {'course_id': self.course.id})
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

        response = self.client.post(url, {'course_id': self.course.id})
        self.assertEqual(response.data['message'], 'Подписка удалена')
