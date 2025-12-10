from django.core.management.base import BaseCommand
from users.models import Payment, CustomUser
from materials.models import Course, Lesson
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create test payments'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        payment_methods = ['cash', 'transfer']

        for i in range(20):
            user = random.choice(users)
            payment_method = random.choice(payment_methods)
            amount = Decimal(random.uniform(100, 10000)).quantize(Decimal('0.01'))

            # Выбираем либо курс, либо урок
            if random.choice([True, False]) and courses:
                course = random.choice(courses)
                lesson = None
            else:
                course = None
                lesson = random.choice(lessons) if lessons else None

            payment_date = datetime.now() - timedelta(days=random.randint(0, 365))

            Payment.objects.create(
                user=user,
                course=course,
                lesson=lesson,
                amount=amount,
                payment_method=payment_method,
                payment_date=payment_date
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 20 payments'))