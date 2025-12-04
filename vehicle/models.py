from django.db import models

class Car(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "машина"
        verbose_name_plural = "машины"
