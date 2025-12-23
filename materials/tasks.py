from materials.models import *

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@shared_task
def send_course_update_email(emails, course_title):
    send_mail(
        subject=f'Обновление курса "{course_title}"',
        message=f'Курс "{course_title}" был обновлён.',
        from_email=None,
        recipient_list=emails,
        fail_silently=False,
    )

# Блокировка пользователей, не заходивших более месяца
User = get_user_model()

@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)

    User.objects.filter(
        last_login__lt=month_ago,
        is_active=True
    ).update(is_active=False)