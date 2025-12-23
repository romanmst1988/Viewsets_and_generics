from materials.models import *

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_email(emails, course_title):
    send_mail(
        subject=f'Обновление курса "{course_title}"',
        message=f'Курс "{course_title}" был обновлён.',
        from_email=None,
        recipient_list=emails,
        fail_silently=False,
    )