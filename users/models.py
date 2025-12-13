from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from materials.models import Course, Lesson
from django.contrib.auth.models import BaseUserManager

from users.permissions import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # type: ignore

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Оплата {self.user.email} — {self.amount}"


