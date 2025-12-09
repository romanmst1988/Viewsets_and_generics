from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey('materials.Course', null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='Оплаченный курс')
    lesson = models.ForeignKey('materials.Lesson', null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email



class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey('materials.Course', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey('materials.Lesson', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    def __str__(self):
        return f"Оплата {self.user.email} — {self.amount}"


